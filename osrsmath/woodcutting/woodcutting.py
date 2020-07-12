from math import exp
from typing import Tuple, Callable, List

LOG_RATE = 2.4
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

# Teak is the only known
# normal, oak, willow, and maple are estimated
# A fit is used to predict Mahogany, yew, magic, and redwood.
# Interestingly, the exponent coefficients seem similar.
def estimate_45(tree_requirement):
	return 45, 0.7945 / exp(0.055*tree_requirement), 'adamant'
def estimate_77(tree_requirement):
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
		'rates': [ estimate_45(50), estimate_77(50) ],
	},
	'yew': {
		'level': 60,
		'log_xp': 175,
		'rates': [ estimate_45(60), estimate_77(60) ],
	},
	'magic': {
		'level': 75,
		'log_xp': 250,
		'rates': [ estimate_45(75), estimate_77(75) ],
	},
	'redwood': {
		'level': 90,
		'log_xp': 380,
		'rates': [ estimate_45(90), estimate_77(90) ],
	},
}

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

def get_xp_rate(tree_name: str, axe_name: str, level: int) -> float:
	""" Calculates the woodcutting experience per hour. 
	
	Args:
		tree_name: The name of the tree to cut.
		axe_name: The name of the axe to use.
		level: The player's woodcutting level

	Returns:
		The experience per hour.
	"""
	# This is the probability of getting a log every LOG_RATE seconds
	P = get_probability(tree_name, axe_name, level)

	# Dividing by the LOG_RATE gives the probability of getting a log every second.
	# This can also be interpreted as the fraction of a log obtained every second.
	logs_per_second = P / LOG_RATE
	return trees[tree_name]['log_xp'] * logs_per_second  * 60*60

def get_probability(tree_name: str, axe_name: str, level: int) -> float:
	""" Calculates the probability of getting a log every `LOG_RATE` seconds.
	
	Args:
		tree_name: The name of the tree to cut.
		axe_name: The name of the axe to use.
		level: The player's woodcutting level

	Returns:
		The probability of getting a log every `LOG_RATE` seconds.
	"""
	# Invalid axes and trees are allowed since some investigations may want that.
	# So it is the responsibility of the caller to ensure the axes and trees can be used.
	tree = trees[tree_name]
	axe = axes[axe_name]
	p1 = convert_axe(tree['rates'][0], axe)
	p2 = convert_axe(tree['rates'][1], axe)
	return max(0, min(interpolate(p1, p2)(level), 1))  # clamp

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


def interpolate(p1: Tuple[int, float], p2: Tuple[int, float]) -> Callable[[int], float]:
	""" Returns a function that linearly interpolates between these two points.

	Implements the equation given in https://mathworld.wolfram.com/Two-PointForm.html
	
	Args:
		p1: A point (x1, y1) with the smaller x value.
		p2: A point (x2, y2) with the larger x value.

	Raises:
		ValueError if x1 is greater than x2.
	"""

	x2, y2 = p2
	x1, y1 = p1
	if x1 >= x2:
		raise ValueError(f"x2 ({x2}) must be greater than x1 ({x1}).")
	slope = (y2 - y1) / (x2 - x1)
	return lambda x: slope*(x - x2) + y2

def get_optimal_training_order(start: int=1, end: int=99):
	""" Determines the optimal trees to train at each level. 

	Args:
		start: The starting level.
		end: The ending level.

	Returns:
		A list containing 2-tuples of the form (level, optimal_tree_to_cut). """
	optimal_order = []
	for level in range(1, 99+1):
		best_tree = max([
			(tree, get_xp_rate(tree, get_best_axe(level), level)) for tree in trees if trees[tree]['level'] <= level],
			key=lambda x: x[1]
		)[0]
		optimal_order.append((level, best_tree))
	return optimal_order[start-1:end+1]


if __name__ == '__main__':
	from pprint import pprint

	get_xp_rate('normal', get_best_axe(1), 1)
	
	pprint(get_optimal_training_order())
	# Normal: 1-14
	# Oak: 15-36
	# Teak: 37-69
	# mahogany 70-99

	
	# This should give 190/255 logs every 2.4 seconds
	# or (190/255)/2.4 logs every second
	# at 85 xp/log this gives 85*(190/255)/2.4 xp/second
	# print(get_xp_rate('teak', 'dragon', 99), 85*(190/255)/2.4 * 60*60)
	# print(get_xp_rate('teak', 'dragon', 1), 85*(60/255)/2.4 * 60*60)
	
	from mpl_toolkits.mplot3d import axes3d
	import matplotlib.pyplot as plt
	import numpy as np
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	def tree_at_level(level):
		for tree, data in trees.items():
			if data['level'] == level:
				return tree
		raise ValueError("No level found")

	@np.vectorize
	def f(x, y):
		return get_xp_rate(tree_at_level(y), get_best_axe(x), x) / 1_000


	x = list(range(1, 99+1))
	y = [data['level'] for tree, data in trees.items()]
	X, Y = np.meshgrid(x, y)
	Z = f(X, Y)
	ax.plot_wireframe(X, Y, Z)

	y = [35]
	X, Y = np.meshgrid(x, y)
	Z = f(X, Y) + 3
	ax.plot_wireframe(X, Y, Z, color='red', linewidth=5)

	y = [50, 60, 75, 90]
	X, Y = np.meshgrid(x, y)
	Z = f(X, Y) + 3
	ax.plot_wireframe(X, Y, Z, color='green', linewidth=5)
	

	plt.xlabel('Woodcutting Level')
	plt.ylabel('Tree Level')
	ax.set_zlabel('Experience Rate [k/h]')
	plt.show()
	# for angle in range(0, 360):
	#     ax.view_init(30, angle)
	#     plt.draw()
	#     plt.pause(.001)

	# print("This is the teak xp rate at 99 using different axes")
	# for axe_name in axes:
	# 	print(axes[axe_name]['level'], get_xp_rate('teak', axe_name, 1))
	# print()

	# print("This is the teak xp rate using the best axe at all levels")
	# for level in range(1, 99+1):
	# 	print(level, get_xp_rate('teak', get_best_axe(level), level))
	# print()