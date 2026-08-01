from osrsmath.general.skills import get_skills
from bs4 import BeautifulSoup
from urllib.parse import quote
from pathlib import Path
import pandas as pd
import requests
import json
import time
import re
import os

WIKI_BASE = "https://runescape.wiki"
WIKI_QUESTS_URL = "https://runescape.wiki/w/List_of_quests"


class WikiQuestListParser:
	# Modified from: https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/

	VALID_TABLES = [1, 3, 4]
	URL_COLUMN = {  # The column that contains the url for the given table.
		1: 1,
		3: 1,
		4: 0  # Table 5 doesn't have an index column.
	}

	def __init__(self):
		self.quest_links = {}
		for table in self.parse_url(WIKI_QUESTS_URL):
			for record in table[["Name", "URL"]].to_dict("records"):
				record["Name"] = record["Name"].replace(',', '')  # "Missing, Presumed Dead" has a ',' in it.
				self.quest_links[record["Name"]] = record["URL"]
		
		self.quest_links = {name: url for name, url in self.quest_links.items() if name != "Recipe for Disaster"}

	def parse_url(self, url):
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'lxml')
		return [self.parse_html_table(i, table) for i, table in enumerate(soup.find_all('table'))]

	def parse_html_table(self, index, table):
		n_columns = 0
		n_rows=0
		column_names = []

		# Find number of rows and columns
		# we also find the column titles if we can
		for row in table.find_all('tr'):
			
			# Determine the number of rows in the table
			td_tags = row.find_all('td')
			if len(td_tags) > 0:
				n_rows+=1
				if n_columns == 0:
					# Set the number of columns for our table
					n_columns = len(td_tags)
					
			# Handle column names if we find them
			th_tags = row.find_all('th') 
			if len(th_tags) > 0 and len(column_names) == 0:
				for th in th_tags:
					column_names.append(th.get_text().strip())  # Modification: Added strip to remove '\n' in title.

		# Safeguard on Column Titles
		if len(column_names) > 0 and len(column_names) != n_columns:
			raise Exception("Column titles do not match the number of columns")

		columns = column_names if len(column_names) > 0 else range(0,n_columns)
		df = pd.DataFrame(columns = columns + ["URL"],  # Modification: Adding URL column
						  index= range(0,n_rows))
		row_marker = 0
		for row in table.find_all('tr'):
			column_marker = 0
			columns = row.find_all('td')
			for i, column in enumerate(columns):
				# Modification: Either the first or second column has the url for the quest.
				# This depends on the table index. Store it when you have it.
				if i == 0:
					quest_url = str(column.contents[0]).split(' ')[1]  # Get html url
					quest_url = quest_url.replace('href="', '')[:-1]  # Get raw url, -1 removes last ".
					df.iat[row_marker, len(columns)] = WIKI_BASE + quest_url  # Add to URL column

				df.iat[row_marker, column_marker] = column.get_text().strip()
				column_marker += 1
			if len(columns) > 0:
				row_marker += 1
				
		# Convert to float if possible
		for col in df:
			try:
				df[col] = df[col].astype(float)
			except ValueError:
				pass
		
		return df


class WikiQuestParser:
	@staticmethod
	def standardize(url):
		for quest in ["Freeing_Pirate_Pete", "Freeing_Skrach_Uglogwee", "Freeing_King_Awowogei", "Freeing_Sir_Amik_Varze", "Freeing_the_Lumbridge_Guide", "Freeing_Evil_Dave", "Freeing_the_Mountain_Dwarf", "Freeing_the_Goblin_generals", "Another_Cook%27s_Quest",]:
			url = url.replace(f"/w/{quest}", f"/w/Recipe_for_Disaster/{quest}")
		url = url.replace('/w/Recipe_for_Disaster"', '/w/Recipe_for_Disaster/Defeating_the_Culinaromancer"')
		return url

	def __init__(self):
		self.quest_links = WikiQuestListParser().quest_links

	def get_quest_data(self):
		start_time = time.time()

		parsed = []
		for i, (name, url) in enumerate(self.quest_links.items(), 1):
			# if i < 250: continue;
			print(f"Parsing Quest #{i} {name}: {url}")
			result = self.parse_link({'name': name, 'url': url}) 
			parsed.append(result)

		end_time = time.time()
		elapsed_time = end_time - start_time
		print(f"Scraped and Parsed {len(self.quest_links)} in {elapsed_time:.2f} seconds.")

		return parsed

	def parse_developer_names(self, raw):
		"""Normalize a developer cell into a list of names (main first).

		Credits often use ';' between people, e.g.
		'Paul Gower; Mod Stu (2017 single player version & improvements)'.
		"""
		raw = raw.split('\n', 1)[0].strip()
		raw = re.sub(r'\([^)]*\)|\[[^\]]*\]', '', raw)
		developers = []
		for part in re.split(r'[;,]', raw):
			name = part.replace('.', '').split(':')[-1].strip()
			name = re.sub(r'\s+feat\b.*', '', name, flags=re.IGNORECASE).strip()
			name = {
				'Unknown': None,
				'Vincent M': 'Vincent van M',
				'Vincent Van M': 'Vincent van M',
			}.get(name, name)
			if name and name not in developers:
				developers.append(name)
		return developers

	def parse_credits_main_developer(self, soup):
		"""Main developer from the Credits section (first/Original table)."""
		def is_credits_table(classes):
			if not classes:
				return False
			parts = classes if isinstance(classes, list) else str(classes).split()
			return 'infobox-credits' in parts

		for table in soup.find_all('table', class_=is_credits_table):
			td = table.find('td', attrs={'data-attr-param': 'developer'})
			if td is None:
				for row in table.find_all('tr'):
					th = row.find('th')
					if th and th.get_text(strip=True).lower() == 'developer':
						td = row.find('td')
						break
			if td is not None:
				return self.parse_developer_names(td.get_text())
		return []

	def parse_link(self, quest_link):
		def find_term(term):
			return x.find("th") and term in x.find("th").get_text().lower()
		def get_value():
			return x.find("td").get_text().strip()

		## This is the small supplementary table.
		details = {"name": quest_link["name"], "url": quest_link["url"], "quest_requirements": [], "skill_requirements": [], "rewards": []}
		response = requests.get(details['url'])
		soup = BeautifulSoup(response.text, 'lxml')

		table = soup.find("table", {"class": "rsw-infobox"}).find('tbody')  # CHANGE 1
		for x in table.find_all("tr"):
			if find_term('release date'):
				details['released'] = get_value().replace("(Update)", "").strip()
			if find_term('members'):
				details['members'] = get_value() == 'Yes'
			if find_term('official series'):
				details['series'] = get_value()
				# print(get_value())
			if find_term('difficulty'):
				details['difficulty'] = get_value()
			if find_term('developer'):  # Rare on RS3; Credits section is preferred below.
				details['developer'] = self.parse_developer_names(get_value())
			if find_term('combat'):  # Infobox: "Combat[?]" → None / enemy summary
				details['combat'] = get_value() != 'None'

		# Credits section (prefer Original / first switch-infobox table).
		credits_devs = self.parse_credits_main_developer(soup)
		if credits_devs:
			details['developer'] = credits_devs
		elif 'developer' not in details:
			details['developer'] = []
					
		## This is the large main table: "Details".
		# Find the Requirements in the questdetails table.
		table = soup.find("table", {"class": "questdetails"}).find('tbody')
		for x in table.find_all("tr"):
			contents = self.standardize(str(x.contents))  # HTML
			if find_term('start'):
				# The last anchor '<a>' in the Start Point text has lat/lon.
				try:  # CHANGE 2
					for anchor in x.findAll("a"):
						if ("data-lat" in str(anchor)) and ("data-lon" in str(anchor)):
							start_location = anchor
							lat, lon = start_location["data-lat"], start_location["data-lon"]
							# Stored as [y, x] (wiki lat/lon == game northing/easting).
							details['start'] = (lat, lon)
							break
					else:
						raise KeyError("No hyper-references have data-lat/data-lon.")
				
				except (KeyError, IndexError):
					match details['name'].lower():
						case 'the blood pact':
							details['start'] = None  # Existing, but not as coords - plain text.
						case 'cold war':
							details['start'] = None  # Existing, but not as coords - plain text.
						case 'desert treasure':
							details['start'] = None  # Existing, but not as coords - plain text.
						case 'dream mentor':
							details['start'] = None  # Existing, but not as coords - plain text.
						case 'glorious memories':
							details['start'] = None  # Existing, but not as coords - plain text.
						case 'goblin diplomacy':
							details['start'] = None  # Existing, but not as coords - plain text.
						case 'legacy of seergaze':
							details['start'] = None  # Existing, but not as coords - plain text.
						case "legends' quest":
							details['start'] = None  # Existing, but not as coords - plain text.
						case "merlin's crystal":
							details['start'] = None  # Existing, but not as coords - plain text.
						case 'rune mysteries':
							details['start'] = None  # Existing, but not as coords - plain text.

						case 'a clockwork syringe':
							details['start'] = None  # Start in POH or Portal.
						case 'regicide':
							details['start'] = None  # Receive a message ~15min after completing Underground Pass.
						case name if name.startswith('rfd') or name.startswith('recipe for disaster'):
							details['start'] = None  # Unspecified by wiki
						case _:
							print("Failed to parse", details['name'])
							raise  # We were unable to identify the start for this quest.


			if find_term('length'):
				details['length'] = get_value()
			if find_term('difficulty'):
				details['difficulty'] = get_value()
			if find_term('enemies') and 'combat' not in details:
				details['combat'] = x.find('td').get_text().strip() != 'None'
			if find_term('requirements'):
				requirements_text = x.get_text().strip()  # Plaintext

				## QUESTS
				# Since partial completions are considered requirements for now, any quest url is a requirement.
				# A slow but easy implementation is to loop through the quest url list and see if any of them are 
				# in the requirements text body. It would be more efficient to identify urls and query those against
				# the quest list. This method fails if a quest is written without a url.
				for name, url in self.quest_links.items():
					if url.replace(WIKI_BASE, '') in contents:
						details["quest_requirements"].append(name)

				## SKILLS
				if any(skill in requirements_text for skill in get_skills()):
					# Every line is a possible skill requirement
					for possible_skill_requirement in requirements_text.split('\n'):
						# Any line contains a skill name, then it may still be a possible requirement.
						if any(skill in possible_skill_requirement for skill in get_skills()):
							skill_requirement_matches = re.findall(fR"(\d+)(\s+)({'|'.join(get_skills())})", possible_skill_requirement)
							if not skill_requirement_matches:
								continue
							
							requirement = first_requirement_in_line = skill_requirement_matches[0]
							level, _, skill,  = requirement
							details["skill_requirements"].append((skill, int(level)))  # Could also capture "(boostable)".

		## Rewards
		reward_element = soup.find(id=lambda x: x == "Rewards" or x == "Reward")
		if reward_element:
			for reward_item in reward_element.find_next("ul").find_all('li'):
				if any(skill in str(reward_item) for skill in get_skills()):
					# Regex fails if over 999,999 experience is awarded.
					experience_reward_matches = re.findall(fR"(\d+,*\d+) +({'|'.join(get_skills())}) experience", reward_item.get_text())
					if experience_reward_matches:
						if len(experience_reward_matches) != 1:  # Multiple values in a single line
							if details['name'] == "Daddy's Home":
								# Reward: 400 Construction experience ... 544 Construction experience is gained when building the furniture, for a total of 944 experience.
								[(xp1, skill), (xp2, _)] = experience_reward_matches
								experience_reward_matches = [
									(str(int(xp1) + int(xp2)), skill)
								]
							else:
								## Choices
								assert details['name'] in [
									"Observatory Quest",   # Random selection; perhaps we treat it like a choice.
									"Tai Bwo Wannai Trio"  # You need to talk to Tamayu to get this reward: it is optional.
								], (details, experience_reward_matches)  # The only existing exception.
								continue  # Ignore due to choices

						experience, skill = reward = experience_reward_matches[0]
						details["rewards"].append((skill, int(experience.replace(',', ''))))

		return details


def load_quest_data(rename: dict, force: bool=False):  # rename {from1: to1, ...}
	file_name = Path(__file__).parent / "parser_files" / "rs3_quest_data.json"
	if force or (not os.path.exists(file_name)):
		json.dump(WikiQuestParser().get_quest_data(), open(file_name, 'w'), indent=4)
		return load_quest_data(rename, force=False)
	else:
		text = open(file_name).read()
		for k, v in rename.items():
			text = text.replace(k, v)
		return json.loads(text)



if __name__ == '__main__':
	# from pprint import pprint
	# pprint(QUEST_URLS)

	# print(WikiQuestParser().parse_url("https://oldschool.runescape.wiki/w/The_Great_Brain_Robbery"))
	# for quest in QUEST_URLS:
	# 	WikiQuestParser(quest["Name"]).parse_url(quest["URL"])

	import argparse
	parser = argparse.ArgumentParser(description='Scrape and Parse the Wiki Quest Data.')
	parser.add_argument('--overwrite', action='store_true', help='Overwrite existing .json.')
	args = parser.parse_args()
	load_quest_data(rename={}, force=args.overwrite)


