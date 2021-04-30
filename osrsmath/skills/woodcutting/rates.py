""" This module contains code related to experience rates. """

from osrsmath.skills.woodcutting.entities import axes, trees, get_best_axe, convert_axe
from math import exp
from typing import Tuple, Callable, List

LOG_RATE = 2.4  # A probability for a log to be obtained occurs every 2.4 seconds.

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


def get_optimal_training_order(start: int=1, end: int=99) -> List[Tuple[int, str]]:
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
