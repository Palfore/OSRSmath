from math import floor
import copy

class BoostingSchemes:
	def __init__(self, player):
		self.player = player

	def potion_when_skill_under(self, potion, skill, min_boost, boosted_skills=('attack', 'strength', 'defence')):
		assert skill in boosted_skills, f'skill: "{skill}" must be in boosted_skills: "{boosted_skills}", otherwise it will never change.'
		boosted_skills = (boosted_skills,) if type(boosted_skills) == str else boosted_skills
		max_boosts = {skill: potion(self.player.levels[skill]) for skill in boosted_skills}
		return get_states(self.player, [
			{skill: max(max_boosts[skill] - t, 0) for skill in boosted_skills}
				for t in range(0, max_boosts[skill] - min_boost + 1)
		])

	def overload(self):
		""" Creates a single boosted state. Although 5 combat skills are boosted, if player does not contain them,
			they will be omitted. """
		boosted_skills=('attack', 'strength', 'defence', 'magic', 'ranged')
		return get_states(self.player, [
			{skill: Potions.overload(self.player.levels[skill]) for skill in boosted_skills if skill in self.player.levels}
		])

	def none(self):
		return get_states(self.player, [{}])

class Potions:
	""" Namespace for different potion boost calculations """
	@staticmethod
	def overload(level):
		return Potions.super(level)

	@staticmethod
	def super(level):
		return floor(0.15*level + 5)

	def normal(level):
		return floor(0.10*level + 3)

	@staticmethod
	def none(_):
		return 0

def get_states(attacker, boosts: list):
	""" @param boost is a list of boosted states. Each element in the list is a dictionary containing the boosted levels. """
	attacker_states = []
	for boost in boosts:
		a = copy.deepcopy(attacker)
		for skill, bonus in boost.items():
			a.levels[skill] += bonus
		attacker_states.append(a)
	return attacker_states

if __name__ == '__main__':
	from osrsmath.model.player import PlayerBuilder

	player = PlayerBuilder({"attack": 70, "strength": 90, "defence": 70}).equip([
		"Dragon Scimitar",
		"Dharok's helm",
		"Dharok's platebody",
		"Dharok's platelegs",
		"Dragon Boots",
		"Holy Blessing",
		"Barrows Gloves",
		"Dragon Defender",
		"Berserker Ring (i)",
		"Amulet of Fury",
		"Fire Cape",
	]).get()
	print("Player")
	player.print()
	print()

	print("Super Combat")
	states = BoostingSchemes(player).super_combat_when_skill_under("attack", 5, 'attack')
	for s in states:
		s.print()
	print()

	print("Overload")
	states = BoostingSchemes(player).overload()
	for s in states:
		s.print()
	print()



