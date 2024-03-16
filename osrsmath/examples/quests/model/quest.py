from osrs_wiki_quest_parser import load_quest_data as load_osrs_data
from rs3_wiki_quest_parser import load_quest_data as load_rs3_data
from osrsmath.general.skills import level as calculate_level
from osrsmath.general.skills import experience as calculate_experience
from osrsmath.general.skills import get_skills

class Skill:
	def __init__(self, xp=None, level=None):
		if xp is None and level is None:
			xp = 0
		if xp is not None and level is not None:
			raise ValueError("To create a skill, supply either an experience amount or a level.")
		
		if level is not None:
			xp = calculate_experience(level)
		elif xp is not None:
			xp = xp
		self.experience = xp

	def gain(self, amount):
		self.experience += amount  # Not capped at 200m here.
	
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
	""" A class representing an in-game quest.
		Mini-Quests are Quests. Achievement Diaries could also be. May even generalize further.
		Requirements: quest, skill, quest_points (ignore), combat (ignore), items (ignore)
		Rewards: experience, quest_points (ignore), items (ignore).
		So, a quest is represented by three vectors.
	"""

	def __init__(self, quest_data, name=None, url=None, released=None, members=None, developer=None, combat=None, series=None, length=None, difficulty=None, skill_requirements=None, quest_requirements=None, rewards=None, completed=False, start=None):
		parameters = locals().copy()  # Create a copy of local variables
		del parameters['self']
		self.__dict__.update(parameters)
		self.skill_requirements = {skill: level for skill, level in skill_requirements} if skill_requirements is not None else {}
		self.quest_requirements = set(quest_requirements) if quest_requirements is not None else set()
		self.rewards = {skill: level for skill, level in rewards} if rewards is not None else {}

		lookup = {q['name']: q for q in self.quest_data}

		# Recursively crawl through all prerequisites
		prereqs = stored_quest_requirements = set(self.quest_requirements)
		while True:  # Keep iterating until no more prereqs are found.
			for name in prereqs:
				prereq_data = lookup[name]
				prereq = Quest(self.quest_data, **prereq_data)

				# For each prereq, accumulate the skill and quest requirements into this quest.
				for skill in list(self.skill_requirements) + list(prereq.skill_requirements):
					self.skill_requirements[skill] = max(self.skill_requirements.get(skill, 0), prereq.skill_requirements.get(skill, 0))
				
				assert name not in prereq.quest_requirements
				self.quest_requirements.union(prereq.quest_requirements)

			if stored_quest_requirements == self.quest_requirements:  # No more prereqs found.
				break
			stored_quest_requirements = self.quest_requirements[:]


	def add_skill_requirement(self, skill, level):
		self.skill_requirements.append((skill, level))

	def add_quest_requirement(self, index):
		self.quest_requirements.append(index)

	def add_experience_reward(self, skill, xp):
		self.rewards[skill] = self.rewards[skill] + xp if skill in self.rewards else xp


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


	def can_be_completed_by(self, player):
		assert len(player.as_vector()) == len(self.get_requirements_as_vector())
		return all(p >= q for p, q in zip(player.as_vector(), self.get_requirements_as_vector()) )

	def __str__(self):
		return str((
			self.skill_requirements, sorted(list(self.quest_requirements))
		))


class QuestBook:
	@staticmethod
	def from_wiki_parser(rs3: bool=False):
		if rs3:
			quest_data = load_rs3_data(rename={'Recipe for Disaster/': 'RFD/'})
		else:
			quest_data = load_osrs_data(rename={'Recipe for Disaster/': 'RFD/'})
		
		quests = {}
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

	def clear(self):
		for n, q in self.quests.items():
			q.completed = False

	def complete(self, identifier):
		self[identifier].completed = True


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
	def create_maxed(rs3: bool=False):
		return Player(Skills.create_uniform_level(99), QuestBook.from_wiki_parser(rs3=rs3))

	@staticmethod
	def create_new_player(rs3: bool=False):
		return Player(Skills.create_new_player(), QuestBook.from_wiki_parser(rs3=rs3))

	@staticmethod
	def create_from_other(other):
		return Player(other.skills, other.quest_book)

	def __init__(self, skills, quest_book):
		self.skills = skills
		self.quest_book = quest_book

	# Queries
	def can_complete(self, quest_identifier):
		return self.quest_book[quest_identifier].can_be_completed_by(self)

	# Actions
	def complete_if_possible(self, quest_identifier):
		blocked = self.quest_book[quest_identifier].name in self.quest_book.blocked
		completable = self.can_complete(quest_identifier)
		possible = completable and not blocked
		if possible:
			self.force_complete(quest_identifier)
		return possible

	def force_complete(self, quest_identifier):
		self.quest_book.complete(quest_identifier)
		self.skills += self.quest_book[quest_identifier].get_reward_as_skills()

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
			quest.can_be_completed_by(self) and
			not quest.completed and
			quest.name not in self.quest_book.blocked
		)]
