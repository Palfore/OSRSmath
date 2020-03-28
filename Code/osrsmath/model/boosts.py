from math import floor
import copy

class Potions:
	""" Namespace for different potion boost calculations.
		These are change in level since potion boosts are additive. """
	@staticmethod
	def overload(level):
		return Potions.super(level)

	@staticmethod
	def super(level):
		return floor(0.15*level + 5)

	def normal(level):
		return floor(0.10*level + 3)

	@staticmethod
	def none(_=None):
		return 0

class Prayers:
	""" Namespace for different prayer boost calculations.
		These are percentage increases in level since prayer boosts are multiplicative. """
	@staticmethod
	def piety(skill):
		multipliers = {
			'attack': 1.20,
			'strength': 1.23,
			'defence': 1.25
		}
		assert skill in multipliers
		return multipliers[skill]

	@staticmethod
	def chivalry(skill):
		multipliers = {
			'attack': 1.15,
			'strength': 1.18,
			'defence': 1.20
		}
		assert skill in multipliers
		return multipliers[skill]

	@staticmethod
	def level3(_=None):
		return 1.15

	@staticmethod
	def level2(_=None):
		return 1.1

	@staticmethod
	def level1(_=None):
		return 1.05

	@staticmethod
	def none(_=None):
		return 1

	@staticmethod
	def rigour(skill):
		multipliers = {
			'ranged': 1.20,
			'ranged_strength': 1.23,
			'defence': 1.25
		}
		assert skill in multipliers
		return multipliers[skill]

	@staticmethod
	def augury(skill):
		multipliers = {
			'magic': 1.25,
			'magic_strength': 1.25,
		}
		assert skill in multipliers
		return multipliers[skill]

class Equipment:
	@staticmethod
	def void(skill):
		multipliers = {
			'strength': 1.10,
			'attack': 1.10,
			'ranged': 1.10,
			'ranged_strength': 1.10,
			'magic': 1.45,
			'magic_strength': 1.0,
		}
		assert skill in multipliers
		return multipliers[skill]

	@staticmethod
	def void_elite(skill):
		multipliers = {
			'strength': 1.10,
			'attack': 1.10,
			'ranged': 1.125,
			'ranged_strength': 1.125,
			'magic': 1.45,
			'magic_strength': 1.025,
		}
		assert skill in multipliers
		return multipliers[skill]


	@staticmethod
	def black_mask(skill):
		multipliers = {
			'strength': 7/6,
			'attack': 7/6,
		}
		assert skill in multipliers
		return multipliers[skill]

	@staticmethod
	def black_mask_i(skill):
		multipliers = {
			'strength': 7/6,
			'attack': 7/6,
			'ranged': 1.15,
			'ranged_strength': 1.15,
			'magic': 1.15,
			'magic_strength': 1.15,
		}
		assert skill in multipliers
		return multipliers[skill]

	@staticmethod
	def obsidian(skill):
		multipliers = {
			'strength': 1.1,
			'attack': 1.1,
		}

class BoostingSchemes:
	def __init__(self, player):
		self.player = player

	def _get_states(attacker, boosts: list):
		""" @param boost is a list of boosted states. Each element in the list is a dictionary containing the boosted levels. """
		attacker_states = []
		for boost in boosts:
			a = copy.deepcopy(attacker)
			for skill, bonus in boost.items():
				a.levels[skill] += bonus
			attacker_states.append(a)
		return attacker_states


	def potion_when_skill_under(self, potion, skill, min_boost, boosted_skills=('attack', 'strength', 'defence')):
		assert skill in boosted_skills, f'skill: "{skill}" must be in boosted_skills: "{boosted_skills}", otherwise it will never change.'
		boosted_skills = (boosted_skills,) if type(boosted_skills) == str else boosted_skills
		max_boosts = {skill: potion(self.player.levels[skill]) for skill in boosted_skills}
		return self._get_states(self.player, [
			{skill: max(max_boosts[skill] - t, 0) for skill in boosted_skills}
				for t in range(0, max_boosts[skill] - min_boost + 1)
		])

	def overload(self):
		""" Creates a single boosted state. Although 5 combat skills are boosted, if player does not contain them,
			they will be omitted. """
		boosted_skills=('attack', 'strength', 'defence', 'magic', 'ranged')
		return self._get_states(self.player, [
			{skill: Potions.overload(self.player.levels[skill]) for skill in boosted_skills if skill in self.player.levels}
		])

	def none(self):
		return self._get_states(self.player, [{}])


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



