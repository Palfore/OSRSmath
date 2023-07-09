from wiki_quest_parser import load_quest_data
from osrsmath.general.skills import level as calculate_level
from osrsmath.general.skills import experience as calculate_experience
from osrsmath.general.skills import get_skills
from pprint import pprint
import itertools as it

class Skill:
	def __init__(self, xp=None, level=None):
		if xp is None and level is None:
			xp = 0
		if xp is not None and level is not None:
			raise ValueError("Can't create a skill using an experience amount and a level.")
		
		if level is not None:
			xp = calculate_experience(level)
		elif xp is not None:
			xp = xp
		self.experience = xp

	def gain(self, amount):
		self.experience += amount
	
	@property
	def level(self):
		return calculate_level(self.experience)


class Skills:
	@staticmethod
	def create_new_player():
		new_player = Skills()
		new_player.add_xp("Hitpoints", calculate_experience(10))
		return new_player

	@staticmethod
	def create_uniform_level(level):
		xp = calculate_experience(level)
		return Skills(xps=[xp for skill in get_skills()])

	@staticmethod
	def create_single(skill, amount):
		single = Skills()
		single.add_xp(skill, amount)
		return single

	def __init__(self, xps=None):
		skill_names = get_skills()
		if xps is None:
			xps = [0]*len(skill_names)
		elif len(xps) != len(skill_names):
				raise ValueError("All skills must be given an experience value.")
		self.skills = {name: Skill(xp) for name, xp in zip(skill_names, xps)}

	def __add__(self, other):
		summed = Skills()
		summed.add_xp_vector(self.as_xp_vector())
		summed.add_xp_vector(other.as_xp_vector())
		return summed

	def add_xp_vector(self, xp_vector):
		if len(xp_vector) != len(self.skills):
			raise ValueError(f"Incorrect xp_vector size, expected {len(self.skills)} got {len(xp_vector)}.")
		for skill, gained_xp in zip(self.skills, xp_vector):
			self.add_xp(skill, gained_xp)

	def add_xp(self, skill, amount):
		self.skills[skill].gain(amount)

	def as_dict(self):
		return {skill: level for skill, level in zip(get_skills(), self.as_level_vector())}

	def as_level_vector(self):
		return [skill.level for skill in self.skills.values()]

	def as_xp_vector(self):
		return [skill.experience for skill in self.skills.values()]


class Quest:
	# Mini-Quests are Quests. Achievement Diaries could also be.
	# Requirements: quest, skill, quest_points, combat, items
	# 	Ignore the latter three for now (i.e. main account that can kill anything, ignoring quest points).
	# Rewards: experience, quest_points, items.
	# 	Ignore the latter two for now.
	# So, a quest is represented by three vectors.
	# quest_data is a code smell, it's only used by encoding and updating prereqs.

	def __init__(self, quest_data, name=None, skill_requirements=None, quest_requirements=None, rewards=None, completed=False):
		self.name = name
		self.quest_data = quest_data
		self.skill_requirements = {skill: level for skill, level in skill_requirements} if skill_requirements is not None else {}
		self.quest_requirements = set(quest_requirements) if quest_requirements is not None else set()
		self.rewards = {skill: level for skill, level in rewards} if rewards is not None else {}
		self.completed = completed


		# Recursively crawl through all prerequisites
		prereqs = stored_quest_requirements = set(self.quest_requirements)
		while True:  # Keep iterating until no more prereqs are found.
			for i, name in enumerate(prereqs):
				prereq_data = self.quest_data[i]
				prereq = Quest(self.quest_data, **prereq_data)

				# For each prereq, accumulate the skill and quest requirements into this quest.
				for skill in list(self.skill_requirements) + list(prereq.skill_requirements):
					self.skill_requirements[skill] = max(self.skill_requirements.get(skill, 0), prereq.skill_requirements.get(skill, 0))
				self.quest_requirements.union(prereq.quest_requirements)

			if stored_quest_requirements == self.quest_requirements:  # No more prereqs found.
				break
			stored_quest_requirements = self.quest_requirements[:]


	def add_skill_requirement(self, skill, level):
		self.skill_requirements.append((skill, level))

	def add_quest_requirement(self, index):
		self.quest_requirements.append(index)

	def add_experience_reward(self, skill, xp):
		if skill not in self.rewards:
			self.rewards[skill] = 0	
		self.rewards[skill] += xp


	def get_skill_requirement_as_skills(self):
		req = Skills()
		for skill, level in self.skill_requirements.items():
			req.add_xp(skill, calculate_experience(level))
		return req

	def get_quest_requirement_as_encoding(self):
		encoding = [False]*len(self.quest_data)
		for quest_req in self.quest_requirements:
			encoding[[d["name"] for d in self.quest_data].index(quest_req)] = True
		return encoding

	def get_reward_as_skills(self):
		reward = Skills()
		for skill, xp in self.rewards.items():
			reward.add_xp(skill, xp)
		return reward

	def get_requirements_as_vector(self):
		return self.get_skill_requirement_as_skills().as_xp_vector() + self.get_quest_requirement_as_encoding()

	def get_as_vector(self):
		return self.get_requirements_as_vector() + self.get_reward_as_skills().as_xp_vector()



	# def meets_quest_requirements(self, player_quests):
	# 	pass

	# def meets_skill_requirements(self, player_skills):
	# 	pass

	def can_be_completed_by(self, player):
		# return self.meets_quest_requirements(self, player.quests) and self.meets_skill_requirements(self, player.skills)
		assert len(player.as_vector()) == len(self.get_requirements_as_vector())
		return all(p >= q for p, q in zip(player.as_vector(), self.get_requirements_as_vector()) )

	def complete(self):
		self.completed = True

	def __str__(self):
		return str((
			self.skill_requirements, sorted(list(self.quest_requirements))
		))

class QuestBook:
	@staticmethod
	def from_wiki_parser():
		# Delete all mention of the quests in remove
		quests = {}
		quest_data = load_quest_data()
		for quest in quest_data:
			quests[quest['name']] = Quest(quest_data, **quest)
		return QuestBook(quests)

	def __init__(self, quests: dict, block:list=None):
		self.quests = quests
		self.blocked = [] if block is None else block

	def __getitem__(self, identifier):
		if isinstance(identifier, str):
			name = identifier
			return self.quests[name]
		elif isinstance(identifier, int):
			index = identifier
			return self.quests[list(self.quests.keys())[index]]
		else:
			raise ValueError(identifier)


	def complete(self, identifier):
		self[identifier].complete()


	def get_quests_requiring(self, prereq_name):
		return [name for name, quest in self.quests.items() if prereq_name in quest.quest_requirements]

	def get_quests_rewarding(self, skill):
		return [name for name, quest in self.quests.items() if skill in quest.rewards]

	def get_quests_with_level_req(self, skill, level, checker="equal"):
		return [name for name, quest in self.quests.items() if {
			"equal": quest.skill_requirements.get(skill, -1) == level,
			"greater": quest.skill_requirements.get(skill, -1) >= level,
			"lesser": quest.skill_requirements.get(skill, -1) <= level,
		}[checker.lower()]]


	def is_complete(self):
		return all(quest.completed for quest in self if quest.name not in self.blocked)
	
	def get_completed(self, status=True):
		return [quest for quest_name, quest in self.quests.items() if quest.completed == status]

	def as_one_hot(self):
		return [quest.completed for quest_name, quest in self.quests.items()]

class Player:
	@staticmethod
	def create_maxed():
		return Player(Skills.create_uniform_level(99), QuestBook.from_wiki_parser())

	@staticmethod
	def create_new_player():
		return Player(Skills.create_new_player(), QuestBook.from_wiki_parser())

	def __init__(self, skills, quest_book):
		self.skills = skills
		self.quest_book = quest_book

	# Queries
	def can_complete(self, identifier):
		return self.quest_book[identifier].can_complete(self)

	# Actions
	def complete_if_possible(self, identifier):
		blocked = player.quest_book[identifier].name in self.quest_book.blocked
		completable = player.quest_book[identifier].can_complete(player)
		possible = completable and not blocked
		if possible:
			player.force_complete(identifier)
		return possible

	def force_complete(self, identifier):
		self.quest_book.complete(identifier)
		self.skills += self.quest_book[identifier].get_reward_as_skills()

	def complete_possible(self):
		i = 0
		previous = set()
		while True:
			# Complete Available Quests
			for quest in self.get_doable_quests():
				self.force_complete(quest)
			
			# Update
			completed = [q.name for q in self.quest_book.get_completed(True)]
			new = set(completed) ^ previous
			if not new:
				break
			previous.update(completed)

	# Retrieval
	def as_vector(self):
		return self.skills.as_xp_vector() + self.quest_book.as_one_hot()

	def get_doable_quests(self):
		return [quest.name for quest in self.quest_book if (
			quest.can_be_completed_by(player) and
			not quest.completed and
			quest.name not in self.quest_book.blocked
		)]


if __name__ == '__main__':
	# Quest book

	# Now I can implement an algorithm that tries to finish the quest cape.
	# I ignore the time it takes to complete a quest, since they all need to be finished.
	# This neglects the fact that some quests may be faster with higher stats (particularly combat).
	# Then, I would need a grid of skill training times.
	# For now, I assume that all skills are trained at the same rate.

	# For the algorithm, I want to train my skills to complete the nearest quest.
	# This isn't correct, since it may be better to strive for a quest with a large payout.
	# But this is a first attempt.
	
	## Algorithm
	# Start with a blank player
	# The player can perform two actions: complete_possible or train_to_nearest.
	# Every iteration, complete_possible then train_to_nearest until all quests are completed.
	# The sum of experience is the cost of the algorithm, multiplying by an average xp rate could yield a time cost.

	def find_nearest_quest(player):
		def prerequisites_are_satisfied(player, quest):  # Should move to quest/player class.
			# Q00100101 (The encoding for the quest requirements)
			# P11001001 (The encoding for the player's completed quests)
			# R11011011 (Whether the requirement is met)

			# If a == 0 -> 1
			# Else if a == b -> 1
			# Else 0

			# Truth Table
			# QPR
			# 001
			# 011
			# 100
			# 111
			# This is "logical implication": https://sites.millersville.edu/bikenaga/math-proof/truth-tables/truth-tables.html
			# Which is the same as "not(a) or b": https://stackoverflow.com/questions/16405892/is-there-an-implication-logical-operator-in-python
			
			p_encoding = player.quest_book.as_one_hot()
			q_encoding = quest.get_quest_requirement_as_encoding()
			return all(not(q) or p for q, p in zip(q_encoding, p_encoding))


		import numpy as np
		nearest_xp = np.inf
		nearest = None
		valid_quests = [quest for quest in player.quest_book.get_completed(False) if prerequisites_are_satisfied(player, quest)]
		for quest in valid_quests:
			distance = np.linalg.norm(
				np.array(player.skills.as_xp_vector()) -
				np.array(quest.get_skill_requirement_as_skills().as_xp_vector())
			)

			if distance < nearest_xp:  # Could be <=
				nearest_xp = distance
				nearest = quest

		xp_required = np.maximum(  # Training to the skill requirements
			np.array(nearest.get_skill_requirement_as_skills().as_xp_vector()) - np.array(player.skills.as_xp_vector()), 0
		)
		cost = sum(xp_required)
		return nearest.name, xp_required, cost

	# Get a quest cape by only training when you need to and by using the nearest quest as the training target.
	# player = Player()
	# cost = 0
	# while not player.quest_book.is_complete():
	# 	player.complete_possible()
		
	# 	nearest, xp_required, penalty = find_nearest_quest(player)
	# 	player.skills += Skills(xp_required)
	# 	player.complete_if_possible(nearest)
	# 	cost += penalty

	# 	print(nearest, f"{penalty:,}", f"{cost:,}", player.skills.as_dict())
	# exit()
	######################################


	import networkx as nx
	from matplotlib import pyplot as plt
	import numpy as np
	from matplotlib.lines import Line2D

	# Obtain the quest shells
	player = Player.create_maxed()
	player.quest_book.blocked.extend(player.quest_book.get_quests_with_level_req("Hitpoints", 10, "greater"))
	player.quest_book.blocked.extend(player.quest_book.get_quests_rewarding("Hitpoints"))
	
	shells = []
	to_complete = player.get_doable_quests()
	while to_complete:
		shells.append(to_complete)
		[player.force_complete(quest) for quest in to_complete]
		to_complete = player.get_doable_quests()
	shell_lookup = {}
	for shell, shell_quests in enumerate(shells):
		for quest in shell_quests:
			shell_lookup[quest] = shell

	# Create a Graph
	g = nx.OrderedMultiDiGraph()
	layout = {}
	for quest in sum(shells, []):
		quest = player.quest_book[quest]

		# Layout
		shell = shell_lookup[quest.name]
		x = shell / len(shells)
		y = shells[shell].index(quest.name) / len(shells[shell])
		layout[quest.name] = np.array([x, y])

		# Graph
		if not quest.quest_requirements:
			g.add_edge(quest.name, quest.name)  # Node
		for prereq in quest.quest_requirements:
			# Only show previous shell connections
			if shell_lookup[prereq] == shell - 1:
				g.add_edge(quest.name, prereq)  # Connection

	# Aesthetics
	connections_are_quest_color = False  # or required quest color
	colors = ['brown', 'orange', 'olive', 'green', 'cyan', 'blue', 'sienna', 'red', 'black', 'orange', 'olive', 'green', 'cyan', 'blue', 'sienna', 'red', 'black', 'black']
	label_dict = {quest: quest.replace("Recipe for Disaster", "RFD") for quest in g}
	node_colors = [colors[shell_lookup[quest]] for quest in g]
	edge_colors = []
	for left, right, info in g.edges:
		choice = [left, right][connections_are_quest_color]
		edge_colors.append(colors[shell_lookup[choice]])

	# Draw the Graph
	plt.title(
		"Old School Runescape Quest Tree\n"+("(colored by quest)" if connections_are_quest_color else "(colored by requirement)"),
		fontsize=20, fontweight="bold"
	)
	nx.draw_networkx(g,
		arrows=True,
		node_size=20,
		font_size=10,
		verticalalignment='bottom',
		width=2,
		arrowsize=20,
		font_weight=1000,

		pos=layout,
		arrowstyle='-|>' if connections_are_quest_color else '<|-',
		edge_color=edge_colors,
		node_color=node_colors,
		labels=label_dict,
	)
	plt.legend(
		[Line2D([0], [0], color=c, linewidth=10, linestyle='-') for c in colors],
		[f"Tier {i} Quest" for i in range(len(shells))],
		fontsize=12
	)

	plt.show()

	######################################
	
	# Two important inverse problems.
	# 1. Get to a skill level through the least amount of training possible.
	# > [quests, training, quests, training, ...]

	# 2. Complete a set of quests through the least amount of training possible.
	# 
	# Both of these are subsets of a common problem:
	# Get a player P to (at least) state G in the least amount of training possible.
	# Since both of these are vectors, the problem is P_i+1 = T_iP_i | min sum_i_training T_i.

	exit()



	# Skills
	try:
		Skill(54, 45)
	except ValueError:
		print("passed")
	print(Skill(level=10).experience)
	print(Skill(level=10).level)


	character = Skills.create_new_player()
	rewards = [
		Skills.create_single("Attack", 1000).as_xp_vector(),
		Skills.create_single("Crafting", 5000).as_xp_vector(),
	]
	for reward in rewards:
		character.add_xp_vector(reward)
	print(character.as_level_vector())
	
	character = Skills.create_new_player()
	rewards = [
		Skills.create_single("Attack", 1000),
		Skills.create_single("Crafting", 5000),
	]
	character = sum(rewards, character)
	print(character.as_level_vector())


	# Quests	
	Legends_Quest = Quest(
		[("Agility", 50)], 
		["Family Crest"],
		[("Agility", 8000)],
	)

	Legends_Quest = Quest()
	Legends_Quest.requires_skill("Agility", 50)
	Legends_Quest.requires_quest("Family Crest")
	Legends_Quest.gives("Agility", 8000)
	print(Legends_Quest.get_reward_as_skill().as_xp_vector())

