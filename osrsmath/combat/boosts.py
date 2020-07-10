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

	@staticmethod
	def normal(level):
		return floor(0.10*level + 3)

	@staticmethod
	def ranging(level):
		return floor(0.10*level + 4)

	@staticmethod
	def magic(_=None):
		return 4

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
	def level3(skill):
		x = 1.15
		multipliers = {
			'attack': x,
			'strength': x,
			'defence': x,
			'ranged': x,
			'ranged_strength': x,
			'magic': x,
		}
		assert skill in multipliers
		return multipliers[skill]

	@staticmethod
	def level2(skill):
		x = 1.1
		multipliers = {
			'attack': x,
			'strength': x,
			'defence': x,
			'ranged': x,
			'ranged_strength': x,
			'magic': x,
		}
		assert skill in multipliers
		return multipliers[skill]

	@staticmethod
	def level1(skill):
		x = 1.05
		multipliers = {
			'attack': x,
			'strength': x,
			'defence': x,
			'ranged': x,
			'ranged_strength': x,
			'magic': x,
		}
		assert skill in multipliers
		return multipliers[skill]

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
		}
		assert skill in multipliers
		return multipliers[skill]

def other(equipment, player):
	equipment = [e.lower() for e in equipment]

	# The order here is important, salve amulet does not stack with black mask
	# The wiki says "only the salve amulet's bonuses will be applied". Not sure
	# if this is because its better, or if it always applies regardless of the variant.
	# Because it's easier to implement, we'll just assume salve takes priority.
	if 'salve amulet (ei)' in equipment:
		return Equipment.salve_amulet_i()
	if 'salve amulet (e)' in equipment:
		return Equipment.salve_amulet()
	if 'salve amulet' in equipment:
		return Equipment.salve_amulet()
	if 'salve amulet (i)' in equipment:
		return Equipment.salve_amulet_i()

	if any(e in equipment for e in ('black mask', 'slayer helmet')):
		return Equipment.black_mask()
	if any(e in equipment for e in ('black mask (i)', 'slayer helmet (i)')):
		return Equipment.black_mask_i()

	if all(e in equipment for e in ('void knight gloves', 'void knight top', 'void knight robe')):
		if 'void melee helm' in equipment:
			return Equipment.void_melee()
		elif 'void ranger helm' in equipment:
			return Equipment.void_ranger()
		elif 'void mage helm' in equipment:
			return Equipment.void_mage()

	if all(e in equipment for e in ('void knight gloves', 'elite void top', 'elite void robe')):
		if 'void melee helm' in equipment:
			return Equipment.elite_void_melee()
		elif 'void ranger helm' in equipment:
			return Equipment.elite_void_ranger()
		elif 'void mage helm' in equipment:
			return Equipment.elite_void_mage()

	if all(e in equipment for e in ("dharok's greataxe", "dharok's helm", "dharok's platebody", "dharok's platelegs")):
		if hasattr(player, 'current_health') and (player.levels['hitpoints'] >= player.current_health > 0):
			return Equipment.dharok(player.levels['hitpoints'] - player.current_health)

	if any(e in equipment for e in ('toktz-xil-ek', 'toktz-xil-ak', 'tzhaar-ket-em', 'tzhaar-ket-om', 'tzhaar-ket-om (t)')):
		if all(e in equipment for e in ('obsidian helmet', 'obsidian platebody', 'obsidian platelegs')):
			if 'berserker necklace' in equipment:
				return Equipment.obsidian_and_necklace()
			else:
				return Equipment.obsidian()
		elif 'berserker necklace' in equipment:
				return Equipment.berserker_necklace()

	return {}

class Equipment:
	@staticmethod
	def none():
		return {
			'strength': 1,
			'attack': 1,
			'defence': 1,
			'ranged': 1,
			'ranged_strength': 1,
			'magic': 1,
			'magic_strength': 1,
		}

	@staticmethod
	def black_mask():
		return {
			'strength': 7/6,
			'attack': 7/6,
		}

	@staticmethod
	def black_mask_i():
		return {
			'strength': 7/6,
			'attack': 7/6,
			'ranged': 1.15,
			'ranged_strength': 1.15,
			'magic': 1.15,
			'magic_strength': 1.15,
		}

	@staticmethod
	def void_melee():
		return {
			'strength': 1.1,
			'attack': 1.1,
		}

	@staticmethod
	def void_ranger():
		return {
			'ranged': 1.1,
			'ranged_strength': 1.1,
		}

	@staticmethod
	def void_mage():
		return {
			'magic': 1.45,
			'magic_strength': 1,
		}

	@staticmethod
	def elite_void_melee():
		return {
			'strength': 1.1,
			'attack': 1.1,
		}


	@staticmethod
	def elite_void_ranger():
		return {
			'ranged': 1.125,
			'ranged_strength': 1.125,
		}


	@staticmethod
	def elite_void_mage():
		return {
			'magic': 1.45,
			'magic_strength': 1.025,
		}

	@staticmethod
	def salve_amulet():
		x = 1.15
		return {
			'attack': x,
			'strength': x,
		}

	@staticmethod
	def salve_amulet_i():
		x = 1.15
		return {
			'attack': x,
			'strength': x,
			'ranged': x,
			'ranged_strength': x,
			'magic': x,
			'magic_strength': x,
		}

	@staticmethod
	def salve_amulet_e():
		x = 1.2
		return {
			'attack': x,
			'strength': x,
		}

	@staticmethod
	def salve_amulet_ei():
		x = 1.2
		return {
			'attack': x,
			'strength': x,
			'ranged': x,
			'ranged_strength': x,
			'magic': x,
			'magic_strength': x,
		}

	@staticmethod
	def obsidian():
		return {
			'strength': 1.1,
			'attack': 1.1,
		}

	@staticmethod
	def berserker_necklace():
		return {
			'strength': 1.2,
			'attack': 1.0,
		}

	@staticmethod
	def obsidian_and_necklace():
		return {
			'strength': 1.3,
			'attack': 1.1,
		}

	@staticmethod
	def dharok(hp_lost):
		return {
			'strength': 1 + (hp_lost / 100)
		}

class BoostingSchemes:
	def __init__(self, player, prayer, prayer_boosted_attributes=('damage', 'accuracy')):
		self.player = player
		self.damage_prayer = prayer if 'damage' in prayer_boosted_attributes else Prayers.none
		self.accuracy_prayer = prayer if 'accuracy' in prayer_boosted_attributes else Prayers.none

	def potion_when_skill_under(self, potion, skill, min_boost, boosted_attributes=('damage', 'accuracy')):
		""" Drink a {potion} that boosts my {boosted_attributues: Note these are generic names since different combat styles are allowed}.
			when my {skill} falls below {min_boost}. """
		max_boost = potion(self.player.levels[skill])
		if min_boost > max_boost:
			raise ValueError(f"A min boost of {min_boost} is too high, the {skill} gets a maximum boost of {max_boost}.")
		return [(
			self.player.get_max_hit(
				(lambda x: max(0, potion(x) - max_boost + boost)) if 'damage' in boosted_attributes else Potions.none,
				self.damage_prayer
			),
			self.player.get_attack_roll(
				(lambda y: max(0, potion(y) - max_boost + boost)) if 'accuracy' in boosted_attributes else Potions.none,
				self.accuracy_prayer
			)
		) for boost in range(min_boost, max_boost+1)]

	def constant(self, potion, boosted_attributes):
		return [(
			self.player.get_max_hit(potion if 'damage' in boosted_attributes else Potions.none, self.damage_prayer),
			self.player.get_attack_roll(potion if 'accuracy' in boosted_attributes else Potions.none, self.accuracy_prayer)
		)]
