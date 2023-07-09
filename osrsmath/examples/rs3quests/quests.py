""" Goal: Implement a tech tree for osrs quests. 

1) Get a list of the quests
2) Get a list of the requirements for each quest
3) Implement a DAG with printing.

Needs:
	BeautifulSoup, networkx, matplotlib

Description:
	Tier 0 quests have no quest requirements.
	In each tier, quests only require quests below that tier.
	Lines are colored by the quest it comes from or goes to, depending on the image.

"""
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import json

WIKI_BASE = "https://oldschool.runescape.wiki/w/"
QUEST_LIST = ["cook's assistant", "demon slayer", "the restless ghost", "romeo & juliet", "sheep shearer", "shield of arrav", "ernest the chicken", "vampyre slayer", "imp catcher", "prince ali rescue", "doric's quest", "black knights' fortress", "witch's potion", "the knight's sword", "goblin diplomacy", "pirate's treasure", "dragon slayer i", "rune mysteries", "misthalin mystery", "the corsair curse", "x marks the spot", "druidic ritual", "lost city", "witch's house", "merlin's crystal", "heroes' quest", "scorpion catcher", "family crest", "tribal totem", "fishing contest", "monk's friend", "temple of ikov", "clock tower", "holy grail", "tree gnome village", "fight arena", "hazeel cult", "sheep herder", "plague city", "sea slug", "waterfall quest", "biohazard", "jungle potion", "the grand tree", "shilo village", "underground pass", "observatory quest", "the tourist trap", "watchtower", "dwarf cannon", "murder mystery", "the dig site", "gertrude's cat", "legends' quest", "big chompy bird hunting", "elemental workshop i", "priest in peril", "nature spirit", "death plateau", "troll stronghold", "tai bwo wannai trio", "regicide", "eadgar's ruse", "shades of mort'ton", "the fremennik trials", "horror from the deep", "throne of miscellania", "monkey madness i", "haunted mine", "troll romance", "in search of the myreque", "creature of fenkenstrain", "roving elves", "ghosts ahoy", "one small favour", "mountain daughter", "between a rock...", "the feud", "the golem", "desert treasure", "icthlarin's little helper", "tears of guthix", "zogre flesh eaters", "the lost tribe", "the giant dwarf", "recruitment drive", "mourning's end part i", "forgettable tale...", "garden of tranquillity", "a tail of two cats", "wanted!", "mourning's end part ii", "rum deal", "shadow of the storm", "making history", "ratcatchers", "spirits of the elid", "devious minds", "the hand in the sand", "enakhra's lament", "cabin fever", "fairytale i - growing pains", "recipe for disaster", "another cook's quest", "defeating the culinaromancer", "freeing the mountain dwarf", "freeing the goblin generals", "freeing pirate pete", "freeing the lumbridge guide", "freeing evil dave", "freeing king awowogei", "freeing sir amik varze", "freeing skrach uglogwee", "in aid of the myreque", "a soul's bane", "rag and bone man i", "rag and bone man ii", "swan song", "royal trouble", "death to the dorgeshuun", "fairytale ii - cure a queen", "lunar diplomacy", "the eyes of glouphrie", "darkness of hallowvale", "the slug menace", "elemental workshop ii", "my arm's big adventure", "enlightened journey", "eagles' peak", "animal magnetism", "contact!", "cold war", "the fremennik isles", "tower of life", "the great brain robbery", "what lies below", "olaf's quest", "another slice of h.a.m.", "dream mentor", "grim tales", "king's ransom", "monkey madness ii", "client of kourend", "bone voyage", "the queen of thieves", "the depths of despair", "dragon slayer ii", "tale of the righteous", "a taste of hope", "making friends with my arm", "the forsaken tower", "the ascent of arceuus", "song of the elves", "the fremennik exiles", "sins of the father", "a porcine of interest", "getting ahead",]
QUEST_LIST.remove("recipe for disaster")
QUEST_LIST.append("alfred grimhand's barcrawl")
QUEST_LIST.append("enter the abyss")

def quest_to_title(quest):
	""" Returns a quest name (lower case) in the proper title format. """
	return quest.title()\
		.replace(' Ii', ' II')\
		.replace("'S", "'s")\
		.replace(' Of ', ' of ')\
		.replace(' The ', ' the ')\
		.replace(' From ', ' from ')\
		.replace(' And ', ' and ')\
		.replace(' In ', ' in ')\
		.replace(' A ', ' a ')\
		.replace(' To ', ' to ')\
		.replace("Mort'Ton", "Mort'ton")

def quest_to_url(quest):
	url = WIKI_BASE + quote(quest_to_title(quest).replace(' ', '_'))
	url = url.replace('Freeing_the_Goblin_Generals', 'Freeing_the_Goblin_generals')  # wiki typo
	return url

class QuestParser:
	def __init__(self, quest):
		self.quest = quest
		self.url = quest_to_url(quest)
		self.content = requests.get(self.url).content
		self.soup = BeautifulSoup(self.content, features="html.parser")

	def get_prerequisite_quests(self):
		# For simplicity, I take partial requirements to be full completions.
		single_quest_phrases = ["Completion of", "Started", "Partial completion of"]
		quest_list_phrases = ["Completion of the following quests", "Must have completed the following quests"]
		table = self.soup.find("table", {"class": "questdetails"}).find('tbody')
		prereqs = []
		for row in table.find_all('tr'):
			if "Requirements" not in row.find('th'):
				continue
			for col in row.find_all('td'):
				for requirement in col.find_all('li'):
					if any(phrase in requirement.text for phrase in quest_list_phrases):
						for quest_tree in requirement.find('ul', recusive=False):
							found = quest_tree.find('a')
							if found != -1:
								prereqs.append(found.text.lower())
					elif any(phrase in requirement.text for phrase in single_quest_phrases):
						if "Started the Firemaking part of Barbarian Training" in requirement.text:  # https://oldschool.runescape.wiki/w/Dragon_Slayer_II
							continue  # Begins with "Started", but isn't a quest

						# Sometimes the statement "Completion of ..." includes a quest symbol, some times it doesn't.
						# This will extract the second item in the list. May not be perfect.
						symbols = requirement.find_all('a')
						assert len(symbols) in (1, 2), (symbols, requirement.text)
						prereq = symbols[-1]
						prereqs.append(prereq.text.lower())
		
		# Modifications:
		if "Pirate Pete" in prereqs:  # From https://oldschool.runescape.wiki/w/The_Great_Brain_Robbery
			prereqs.remove("Pirate Pete")
			prereqs.append("Freeing Pirate Pete")

		return prereqs

	def get_all_prerequisite_quests(self):
		prereqs = self.get_prerequisite_quests()
		for prereq in prereqs:
			new_prereqs = QuestParser(prereq).get_prerequisite_quests()
			prereqs.extend(new_prereqs)
		return set(prereqs)


# class Quest:
# 	def __init__(self, name):
# 		self.name = name
# 		self.id
# 		self.url
# 		self.length
# 		self.description
# 		self.difficulty
# 		self.released
# 		self.members
# 		self.series

# 	def required_quests(self):

# 	def all_required_quests(self, quest_list):
# 		pass

# 	def skill_requirements(self):
# 		pass

# 	def unlocks(self, quest_list):
# 		pass



class QuestList:
	@staticmethod
	def from_json(path):
		return QuestList(json.load(open(path)))

	def __init__(self, quest_data):
		self.quests = quest_data

	def get_quests_with_no_requirements(self):
		return self.get_quests_with_these_requirements([])

	def get_quests_with_these_requirements(self, allowed_quest_requirements):
		allowed_quest_requirements = list(map(str.lower, allowed_quest_requirements))
		return [q for q, reqs in self.quests.items()
				if all(req.lower() in allowed_quest_requirements for req in reqs)]


if __name__ == "__main__":
	from matplotlib import pyplot as plt
	from matplotlib.lines import Line2D
	from pprint import pprint
	import networkx as nx
	import numpy as np
	import json

	file_name = "quest_requirements.json"
	
	# Saving
	# quests = {}
	# for i, quest in enumerate(QUEST_LIST, 1):
	# 	print(f"{i}/{len(QUEST_LIST)}, {quest}")
	# 	quests[quest] = []
	# 	for prereq in QuestParser(quest).get_prerequisite_quests():
	# 		quest = quest.replace("", "")
	# 		prereq = prereq.replace("", "")
	# 		quests[quest].append(prereq)
	# json.dump(quests, open("quest_requirements.json", "w"))
	# print("Saved")

	# Plotting
	quest_list = QuestList.from_json(file_name)
	allowed_quests = set()
	shells = []
	layout = {}
	for i in range(10):
		all_quests = quest_list.get_quests_with_these_requirements(allowed_quests)
		diff = set(all_quests) ^ allowed_quests
		diff = list(reversed(sorted(list(diff))))  # sort
		shells.append([])
		for j, quest in enumerate(diff, 1):
			shells[-1].append(quest)
			layout[quest] = np.array([i/10, j/(len(diff)+1)])
		allowed_quests.update(all_quests)
	shells.reverse()

	print(shells)
	print(len(allowed_quests))

	# Loading
	graph_data = []
	quests = json.load(open(file_name))
	for quest, prereqs in quests.items():
		if prereqs:
			for prereq in prereqs:
				graph_data.append((quest, prereq))
		else:
			graph_data.append((quest, quest))

	# Creating Graph
	connections_are_quest_color = True  # or required quest color
	plt.figure(figsize=(60, 80))
	plt.title(
		"Old School Runescape Quest Tree\n"+("(colored by quest)" if connections_are_quest_color else "(colored by requirement)"),
		fontsize=150, fontweight="bold"
	)
	g = nx.OrderedMultiDiGraph()
	colors = ['brown', 'orange', 'olive', 'green', 'cyan', 'blue', 'sienna', 'red', 'black', 'black']
	
	# Edge colors
	edge_colors = []
	for d in graph_data:
		q1, q2 = d
		
		# Broken, temporary fix!
		q1 = q1.replace("recipe for disaster/", "")
		q2 = q2.replace("recipe for disaster/", "")

		g.add_edge(q1, q2)
		for i, shell in enumerate(shells):
			q = q1 if connections_are_quest_color else q2
			if q in shell:
				edge_colors.append(colors[i])
				break

	# Node colors
	node_colors = []
	for node in g:
		for i, shell in enumerate(shells):
			if node in shell:
				node_colors.append(colors[i])

	# Node Labels
	label_dict = {node: quest_to_title(node) for node in g}

	# Broken, temporary fix! 
	layout['ghostspeak amulet'] = np.array([0., 0.])
	layout['pirate pete'] = np.array([0., 0.])
	layout['recipe for disaster'] = np.array([0., 0.])
	for quest in QUEST_LIST:
		if quest not in layout:
			layout[quest] = np.array([0, 0.])
	
	# Create network
	nx.draw_networkx(g,
		arrows=True,
		node_size=1200,
		font_size=40,
		verticalalignment='bottom',
		width=2,
		arrowsize=50,
		font_weight=1000,
		
		pos=layout,
		arrowstyle='-|>' if connections_are_quest_color else '<|-',
		edge_color=edge_colors,
		# node_color=node_colors,  broken
		labels=label_dict,
	)
	
	# Add custom legend
	lines = [Line2D([0], [0], color=c, linewidth=20, linestyle='-') for c in colors]
	plt.legend(
		lines,
		[f"Tier {len(colors) - i} Quest" for i, c in enumerate(colors, 1)],
		fontsize=80
	)

	# Save plot
	plt.axis('off')
	plt.tight_layout()
	plt.savefig(f"by_{'quest' if connections_are_quest_color else 'requirement'}.pdf", format="pdf")

	