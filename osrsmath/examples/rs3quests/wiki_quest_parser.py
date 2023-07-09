from osrsmath.general.skills import get_skills
from bs4 import BeautifulSoup
from urllib.parse import quote
import pandas as pd
import requests
import json
import re


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
		self.quest_links = []
		for table in self.parse_url(WIKI_QUESTS_URL):
			print(table)
			self.quest_links.extend(table[["Name", "URL"]].to_dict("records"))

		self.quest_links = [quest for quest in self.quest_links if quest['Name'] != "Recipe for Disaster"]

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
		url = url.replace("/w/Freeing_Pirate_Pete", "/w/Recipe_for_Disaster/Freeing_Pirate_Pete")
		url = url.replace("/w/Freeing_Skrach_Uglogwee", "/w/Recipe_for_Disaster/Freeing_Skrach_Uglogwee")
		url = url.replace("/w/Freeing_King_Awowogei", "/w/Recipe_for_Disaster/Freeing_King_Awowogei")
		url = url.replace("/w/Freeing_Sir_Amik_Varze", "/w/Recipe_for_Disaster/Freeing_Sir_Amik_Varze")
		url = url.replace("/w/Freeing_the_Lumbridge_Guide", "/w/Recipe_for_Disaster/Freeing_the_Lumbridge_Guide")
		url = url.replace("/w/Freeing_Pirate_Pete", "/w/Recipe_for_Disaster/Freeing_Pirate_Pete")
		url = url.replace("/w/Freeing_Evil_Dave", "/w/Recipe_for_Disaster/Freeing_Evil_Dave")
		url = url.replace("/w/Freeing_the_Mountain_Dwarf", "/w/Recipe_for_Disaster/Freeing_the_Mountain_Dwarf")
		url = url.replace("/w/Freeing_the_Goblin_generals", "/w/Recipe_for_Disaster/Freeing_the_Goblin_generals")
		url = url.replace("/w/Another_Cook%27s_Quest", "/w/Recipe_for_Disaster/Another_Cook%27s_Quest")
		url = url.replace('/w/Recipe_for_Disaster"', '/w/Recipe_for_Disaster/Defeating_the_Culinaromancer"')
		return url

	def __init__(self, quest_urls):
		self.quest_urls = quest_urls

	def parse_link(self, quest_link):
		name = quest_link["Name"]
		url = quest_link["URL"]
		quest_requirements = []
		skill_requirements = []
		rewards = []

		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'lxml')

		# Find the Requirements in the questdetails table.
		try:
			table = soup.find("table", {"class": "questdetails"}).find('tbody')
		except AttributeError:
			print(quest_link)
			return {
				"name": name,
				"quest_requirements": {},
				"skill_requirements": {},
				"rewards": {},
			}


		for x in table.find_all("tr"):
			contents = self.standardize(str(x.contents))  # HTML
			if not x.find("th"):  # Typically, an empty page
				continue
			if x.find("th").get_text() == "Requirements":
				requirements_text = x.get_text().strip()  # Plaintext

				## QUESTS
				# Any time there is a quest url, it is a requirement.
				# If the line containing the url has any "Partial Completion" terms, then it would be considered partial.
				# Except for exception listed in the organized.txt. However, since we are treating partial completions 
				# as requirements for now, any quest url is a requirement. So just extract urls that are quest_urls.
				# This method fails if the quest is written without a url.
				
				# A slow but easy implementation is to loop through the quest url list and see if any of them are 
				# in the requirements text body. It would be more efficient to identify urls and query those against
				# the quest list.
				for quest in self.quest_urls:
					if quest["URL"].replace(WIKI_BASE, '') in contents:
						quest_requirements.append(quest["Name"])

				## SKILLS
				# Let me see what every line that has a skill looks like.
				if any(skill in requirements_text for skill in get_skills()):
					for possible_skill_requirement in requirements_text.split('\n'):
						if any(skill in possible_skill_requirement for skill in get_skills()):
							# Any text in the following format is taken to be a skill requirement:
							# 	Number Skill_Name supplementary_information
							matches = re.findall(fR"(\d+)(\s+)({'|'.join(get_skills())})", possible_skill_requirement)
							if not matches:
								continue
							
							# Ignore skills requirements that follow the initial statement since these are supplementary.						
							requirement = first_requirement_in_line = matches[0]
							level, _, skill = requirement

							# It is ignored for now and skills are taken to be unboostable.
							# Could also capture "(boostable)".
							skill_requirements.append((skill, int(level)))

		## Rewards
		reward_element = soup.find(id=lambda x: x == "Rewards" or x == "Reward")
		if reward_element:
			for reward_item in reward_element.find_next("ul").find_all('li'):
				if any(skill in str(reward_item) for skill in get_skills()):
					# Any text in the following format is taken to be an experience reward:
					# 	#,###[whitespace]Skill_Name experience  Will fail if over 999,999 experience is awarded.
					matches = re.findall(fR"(\d+,*\d+) +({'|'.join(get_skills())}) experience", reward_item.get_text())

					if matches:
						if len(matches) != 1:
							assert name == "Observatory Quest", name
							continue  # Ignore due to choices

						experience, skill = reward = matches[0]
						rewards.append((skill, int(experience.replace(',', ''))))

		return {
			"name": name,
			"quest_requirements": quest_requirements,
			"skill_requirements": skill_requirements,
			"rewards": rewards,
		}


def load_quest_data():
	import json
	import os

	file_name = "quest_data.json"
	if os.path.exists(file_name):
		return json.load(open(file_name))
	else:
		quest_links = WikiQuestListParser().quest_links
		quest_data = [WikiQuestParser(quest_links).parse_link(link) for link in quest_links]
		json.dump(quest_data, open(file_name, 'w'), indent=4)


if __name__ == '__main__':
	# from pprint import pprint
	# pprint(QUEST_URLS)

	# print(WikiQuestParser().parse_url("https://oldschool.runescape.wiki/w/The_Great_Brain_Robbery"))
	# for quest in QUEST_URLS:
	# 	WikiQuestParser(quest["Name"]).parse_url(quest["URL"])
	load_quest_data()


