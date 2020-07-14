""" This module contains tree and axe information. """

from math import exp
from typing import Tuple, List

def get_best_axe(level: int, ignores: List[str]=None) -> str:
	""" Returns the best axe the player can use.
	
	Args:
		level: The player's woodcutting level. 
		ignores: A list of axes to ignore.

	Returns:
		The name of the best axe the player can use.
	"""
	for axe_name, stats in reversed(axes.items()):
		if ignores and axe_name in ignores:
			continue
		if level >= stats['level']:
			return axe_name
	raise ValueError("No axe was found.")

def convert_axe(rate: Tuple[int, float, str], axe: dict) -> Tuple[int, float]:
	""" Converts the rate of an arbitrary axe to the rate with the desired axe.
	
	Args:
		rate: A 3-tuple of the form (level, probability, axe_name)
		axe: The desired axe with keys 'level' and 'multiplier'

	Returns:
		A 2-tuple of the form (level, probability).
	 """
	# Convert every rate to bronze, then convert to desired axe.
	# A good test case would be that the converting to the same axe returns the input.
	level, probability, known_axe = rate
	return level, axe['multipler'] * probability / axes[known_axe]['multipler']

# Teak is the only known
# normal, oak, willow, and maple are estimated
# A fit is used to predict Mahogany, yew, magic, and redwood.
# Interestingly, the exponent coefficients seem similar.
def _estimate_45(tree_requirement):
	return 45, 0.7945 / exp(0.055*tree_requirement), 'adamant'
def _estimate_77(tree_requirement):
	return 77, 1.7413 / exp(0.051*tree_requirement), 'bronze'

trees = {
	'normal': {
		'level': 1,
		'log_xp': 25,
		'rates': [ (45, 0.325842697, 'bronze'), (77, 0.75862069, 'bronze') ],
	},
	'oak': {
		'level': 15,
		'log_xp': 37.5,
		'rates': [ (45, 0.809638554, 'adamant'), (77, 0.32920354, 'bronze') ],
	},
	'willow': {
		'level': 30,
		'log_xp': 67.5,
		'rates': [ (45, 0.379661017, 'adamant'), (77, 0.167307692, 'bronze') ],
	},
	'teak': {
		'level': 35,
		'log_xp': 85,
		'rates': [ (1, 60/255, 'dragon'), (99, 190/255, 'dragon') ],
	},
	'maple': {
		'level': 45,
		'log_xp': 100,
		'rates': [ (45, 0.175774648, 'adamant'), (77, 0.064468864, 'bronze') ],
	},
	'mahogany': {
		'level': 50,
		'log_xp': 125,
		'rates': [ _estimate_45(50), _estimate_77(50) ],
	},
	'yew': {
		'level': 60,
		'log_xp': 175,
		'rates': [ _estimate_45(60), _estimate_77(60) ],
	},
	'magic': {
		'level': 75,
		'log_xp': 250,
		'rates': [ _estimate_45(75), _estimate_77(75) ],
	},
	'redwood': {
		'level': 90,
		'log_xp': 380,
		'rates': [ _estimate_45(90), _estimate_77(90) ],
	},
}
""" A dictionary containing useful tree information. The keys are the tree names e.g. 'maple'. """

axes = {
	'bronze': {
		'level': 1,
		'multipler': 1
	},
	'iron': {
		'level': 1,
		'multipler': 1.5
	},
	'steel': {
		'level': 6,
		'multipler': 2
	},
	'black': {
		'level': 11,
		'multipler': 2.25
	},
	'mithril': {
		'level': 21,
		'multipler': 2.5
	},
	'adamant': {
		'level': 31,
		'multipler': 3
	},
	'rune': {
		'level': 41,
		'multipler': 3.5
	},
	'dragon': {
		'level': 61,
		'multipler': 3.75
	},
	'crystal': {
		'level': 71,
		'multipler': 4  # 3.91875 or 4.025 based on https://oldschool.runescape.wiki/w/Crystal_axe
		                # Due to those coming from rounded numbers, the true value is likely 4.
	},
}
""" A dictionary containing useful axe information. The keys are the axe type e.g. 'bronze'. """

