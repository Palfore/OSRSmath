""" This module provides useful information about the skills. """

from math import floor


EXPERIENCE_TABLE = {
	1: 0, 2: 83, 3: 174, 4: 276, 5: 388, 6: 512, 7: 650, 8: 801, 9: 969, 10: 1_154, 11: 1_358, 12: 1_584, 13: 1_833, 
	14: 2_107, 15: 2_411, 16: 2_746, 17: 3_115, 18: 3_523, 19: 3_973, 20: 4_470, 21: 5_018, 22: 5_624, 23: 6_291, 
	24: 7_028, 25: 7_842, 26: 8_740, 27: 9_730, 28: 10_824, 29: 12_031, 30: 13_363, 31: 14_833, 32: 16_456, 33: 18_247,
	34: 20_224, 35: 22_406, 36: 24_815, 37: 27_473, 38: 30_408, 39: 33_648, 40: 37_224, 41: 41_171, 42: 45_529,
	43: 50_339, 44: 55_649, 45: 61_512, 46: 67_983, 47: 75_127, 48: 83_014, 49: 91_721, 50: 101_333, 51: 111_945,
	52: 123_660, 53: 136_594, 54: 150_872, 55: 166_636, 56: 184_040, 57: 203_254, 58: 224_466, 59: 247_886, 60: 273_742,
	61: 302_288, 62: 333_804, 63: 368_599, 64: 407_015, 65: 449_428, 66: 496_254, 67: 547_953, 68: 605_032, 69: 668_051,
	70: 737_627, 71: 814_445, 72: 899_257, 73: 992_895, 74: 1_096_278, 75: 1_210_421, 76: 1_336_443, 77: 1_475_581,
	78: 1_629_200, 79: 1_798_808, 80: 1_986_068, 81: 2_192_818, 82: 2_421_087, 83: 2_673_114, 84: 2_951_373,
	85: 3_258_594, 86: 3_597_792, 87: 3_972_294, 88: 4_385_776, 89: 4_842_295, 90: 5_346_332, 91: 5_902_831,
	92: 6_517_253, 93: 7_195_629, 94: 7_944_614, 95: 8_771_558, 96: 9_684_577, 97: 10_692_629, 98: 11_805_606,
	99: 13_034_431, 100: 14_391_160, 101: 15_889_109, 102: 17_542_976, 103: 19_368_992, 104: 21_385_073,
	105: 23_611_006, 106: 26_068_632, 107: 28_782_069, 108: 31_777_943, 109: 35_085_654, 110: 38_737_661,
	111: 42_769_801, 112: 47_221_641, 113: 52_136_869, 114: 57_563_718, 115: 63_555_443, 116: 70_170_840,
	117: 77_474_828, 118: 85_539_082, 119: 94_442_737, 120: 104_273_167, 121: 115_126_838, 122: 127_110_260,
	123: 140_341_028, 124: 154_948_977, 125: 171_077_457, 126: 188_884_740,
}
EXPERIENCE_CAP = 200_000_000
EXPERIENCE_MIN = 0
LEVEL_CAP = 99
LEVEL_MIN = 1
VIRTUAL_LEVEL_CAP = max(EXPERIENCE_TABLE)

def experience(level: int, virtual_levels: bool=False):
	""" Returns the experience required to be at a given level.
	
	Args:
		level: The level to determine the experience requirement for.
		virtual_levels: Whether levels above 99 should be allowed.

	Raises:
		ValueError If the level is out of bounds, i.e. not a valid in-game level. If virtual_levels is True,
		     the bounds increase from LEVEL_CAP to VIRTUAL_LEVEL_CAP.
	"""
	if level < LEVEL_MIN:
		raise ValueError(f"Level ({level}) must be at least {LEVEL_MIN}.")
	if level > LEVEL_CAP and not virtual_levels:
		raise ValueError(f"Level ({level}) cannot exceed the level cap of {LEVEL_CAP} (Try passing `virtual_levels` as True).")
	if level > VIRTUAL_LEVEL_CAP:
		raise ValueError(f"Level ({lavel}) cannot exceed the virtual level cap of {VIRTUAL_LEVEL_CAP}.")
	return EXPERIENCE_TABLE[level]

def level(experience: float, virtual_levels: bool=False):
	""" Returns the level associated with an amount of experience.
	
	Args:
		level: The experience to determine the level for. If virtual_levels is False, 
		    levels will be capped by LEVEL_CAP.
		virtual_levels: Whether levels above 99 should be allowed.

	Raises:
		ValueError If experience is out of bounds, i.e. not a valid in-game experience.
	"""
	if experience < EXPERIENCE_MIN:
		raise ValueError(f"Experience ({experience}) must be at least {EXPERIENCE_MIN}.")
	if experience > EXPERIENCE_CAP:
		raise ValueError(f"Experience ({experience}) cannot exceed the experience cap of {EXPERIENCE_CAP}.")
	if not virtual_levels and experience > EXPERIENCE_TABLE[LEVEL_CAP]:
		return LEVEL_CAP

	for l, xp in reversed(EXPERIENCE_TABLE.items()):
		if experience >= xp:
			return l
	raise AssertionError(f"Something went wrong while calculating the level from xp {experience} with virtual_levels={virtual_levels}.")

def get_skills(lower: bool=False):
	""" Returns a list of the skill names in the order listed on the highscores.
	
	See https://secure.runescape.com/m=hiscore_oldschool/overall

	Args:
		lower: If the skills should be lowercase or titlecase. """
	skills = [
		"Attack",
		"Defence",
		"Strength",
		"Hitpoints",
		"Ranged",
		"Prayer",
		"Magic",
		"Cooking",
		"Woodcutting",
		"Fletching",
		"Fishing",
		"Firemaking",
		"Crafting",
		"Smithing",
		"Mining",
		"Herblore",
		"Agility",
		"Thieving",
		"Slayer",
		"Farming",
		"Runecraft",
		"Hunter",
		"Construction"
	]
	return [s.lower() for s in skills] if lower else skills

def get_combat_skills(lower: bool=False):
	""" Returns a list of the skills that contribute to combat level in no particular order.
		
	Args:
		lower: If the skills should be lowercase or titlecase. """
	skills = [
		"Attack",
		"Strength",
		"Defence",
		"Hitpoints",
		"Ranged",
		"Magic",
		"Prayer"
	]
	return [s.lower() for s in skills] if lower else skills

def combat_level(stats: dict, integer=True):
	required_stats = ('attack', 'strength', 'defence', 'hitpoints', 'prayer', 'ranged', 'magic')
	for s in required_stats:
		if s not in stats:
			raise ValueError(f"You must provide the {s} level to be able to calculate combat level.")
	base = 0.25 * (stats['defence'] + stats['hitpoints'] + floor(stats['prayer'] / 2))
	melee = 0.325 * (stats['attack'] + stats['strength'])
	ranged = 0.325 * floor(3*stats['ranged']/2)
	mage = 0.325 * floor(3*stats['magic']/2)
	level = base + max(melee, ranged, mage)
	return floor(level) if integer else level
