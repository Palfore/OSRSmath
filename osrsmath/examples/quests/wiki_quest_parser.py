from osrsmath.general.skills import get_skills
from bs4 import BeautifulSoup
from urllib.parse import quote
import pandas as pd
import requests
import json
import re
import os
import itertools

WIKI_BASE = "https://oldschool.runescape.wiki"
WIKI_QUESTS_URL = "https://oldschool.runescape.wiki/w/Quests/List"


class WikiQuestListParser:
	def __init__(self):
		link_column = {1: 1, 3: 1, 4: 0}
		html_tables = BeautifulSoup(requests.get(WIKI_QUESTS_URL).text, features="lxml").find_all('tbody')
		self.quest_links = {}
		for name_column, table in [(name_column, html_tables[valid_table]) for valid_table, name_column in link_column.items()]:
			for quest_row in [row for row in table.findAll('tr') if row.findAll('td')]:  # Ignore headers
				x = row.findAll('td')[name_column].contents[0]
				self.quest_links[x.contents[0]] = WIKI_BASE + x.get('href')
		del self.quest_links['Recipe for Disaster']


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
		return [self.parse_link({'name': name, 'url': url}) for name, url in self.quest_links.items()]

	def parse_link(self, quest_link):
		def find_term(term):
			return x.find("th") and term in x.find("th").get_text().lower()
		def get_value():
			return x.find("td").get_text().strip()

		details = {"name": quest_link["name"], "url": quest_link["url"], "quest_requirements": [], "skill_requirements": [], "rewards": []}
		response = requests.get(details['url'])
		soup = BeautifulSoup(response.text, 'lxml')
		table = soup.find("table", {"class": "infobox"}).find('tbody')
		for x in table.find_all("tr"):
			if find_term('released'):
				details['released'] = get_value().replace("(Update)", "").strip()
			if find_term('members'):
				details['members'] = get_value() == 'Yes'
			if find_term('series'):
				details['series'] = get_value()
			if find_term('difficulty'):
				details['difficulty'] = get_value()
			if find_term('developer'):  # We just want the raw names.
				# Remove spaces, periods (used in abbreviations), text on left of : is the developers role which is discarded. Then remove text in [] or ().
				details['developer'] = [re.sub(R"[\(\[].*?[\)\]]", "", d.replace('.', '').split(':')[-1]).strip() for d in get_value().split(',')]
				
		# Find the Requirements in the questdetails table.
		table = soup.find("table", {"class": "questdetails"}).find('tbody')
		for x in table.find_all("tr"):
			contents = self.standardize(str(x.contents))  # HTML
			if find_term('length'):
				details['length'] = get_value()
			if find_term('difficulty'):
				details['difficulty'] = get_value()
			if find_term('enemies'):
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
							assert details['name'] == "Observatory Quest", details  # The only existing exception.
							continue  # Ignore due to choices

						experience, skill = reward = experience_reward_matches[0]
						details["rewards"].append((skill, int(experience.replace(',', ''))))

		return details


def load_quest_data(rename: dict):  # rename {from1: to1, ...}
	file_name = "quest_data.json"
	if os.path.exists(file_name):
		text = open(file_name).read()
		for k, v in rename.items():
			text = text.replace(k, v)
		return json.loads(text)
	else:
		json.dump(WikiQuestParser().get_quest_data(), open(file_name, 'w'), indent=4)


if __name__ == '__main__':
	load_quest_data()
