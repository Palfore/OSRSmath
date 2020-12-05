from osrsmath.general.skills import LEVEL_CAP, EXPERIENCE_CAP, level, experience
from math import ceil

ACTIONS = {
	'lighting': {
		'points': 25,
		'multiplier': 6.0
	},
	'chop': {
		'points': 0,
		'multiplier': 0.3
	},
	'root': {
		'points': 10,
		'multiplier': 3.0
	},
	'kindling': {
		'points': 25,
		'multiplier': 3.8
	},
	'fletching': {
		'points': 0,
		'multiplier': 0.6
	},
	'fixing': {
		'points': 25,
		'multiplier': 4.0  # Assuming player has poh
	},
	'picking': {
		'points': 0,
		'multiplier': 0.1
	},
	'potion': {
		'points': 0,
		'multiplier': 0.1
	},
	'healing': {
		'points': 30,
		'multiplier': 0.0
	},
	'bonus': {
		'points': 0,
		'multiplier': 100.0
	},
	
}
POINT_AWARDING_ACTIONS = [action for action, details in ACTIONS.items() if details['points'] > 0]
POINTS_REQUIRED = 500
BURNING_ACTIONS = ['root', 'kindling']
REQUIRED_LEVEL = 50


class Firemaker:
	def __init__(self, initial_fm_xp, policy=None):
		starting_level = level(initial_fm_xp)
		if starting_level < REQUIRED_LEVEL:
			raise ValueError(f"Wintertodt can only be fought after level {REQUIRED_LEVEL} firemaking, level {starting_level} is too low.")
		if policy is None:
			policy = Policies.kindling_till_bonus
		
		self.E0 = initial_fm_xp
		self.xp = self.E0
		self.policy = policy
		
	def perform_action(self, action, n=1):
		if action in BURNING_ACTIONS:
			return self.burn(action, n=n)
		raise NotImplementedError("Only burning actions are currently supported.")

	def burn(self, item, n=1):
		if n < 0:
			raise ValueError(f"Cannot perform a negative number ({n}) of actions.")
		if item not in BURNING_ACTIONS:
			raise ValueError(f"Can only burn {BURNING_ACTIONS}, not {item}.")
		for _ in range(n):
			self._gain_xp(ACTIONS[item]['multiplier'] * level(self.xp))
		return self.xp

	def kill(self, target_points=500):
		if target_points < 0:
			raise ValueError(f"Cannot obtain a negative amount ({target_points}) of points.")
			
		# Carry out the actions within the fight.
		for action, count in self.policy(self, target_points):
			self.perform_action(action, n=count)

		# If you win, gain the bonus experience.
		if target_points >= POINTS_REQUIRED:
			self._gain_xp(bonus_experience(self.xp))
		return self.xp

	def _gain_xp(self, xp):
		self.xp = min(round(self.xp + xp, 1), EXPERIENCE_CAP)


class Policies:
	""" Returns a sequence of actions in terms of (action, count) pairs. """

	@staticmethod
	def roots_only(firemaker, target_points):
		n = actions_to_target('root', target_points)
		return [('root', n)] if n > 0 else []

	@staticmethod
	def kindling_only(firemaker, target_points):
		n = actions_to_target('kindling', target_points)
		return [('kindling', n)] if n > 0 else []

	@staticmethod
	def kindling_till_x(firemaker, target_points, x):
		num_kindling = actions_to_target('kindling', min(x, target_points))
		points_from_kindling = ACTIONS['kindling']['points'] * num_kindling
		points_remaining = max(target_points - points_from_kindling, 0)
		num_roots = actions_to_target('root', points_remaining)
		points_from_roots = ACTIONS['kindling']['points'] * num_roots
		assert points_from_kindling + points_from_roots >= target_points
		return ([('kindling', num_kindling)] if num_kindling > 0 else []) + ([('root', num_roots)] if num_roots > 0 else [])

	@staticmethod
	def kindling_till_bonus(firemaker, target_points):
		return Policies.kindling_till_x(firemaker, target_points, POINTS_REQUIRED)


def actions_to_target(action, target_points):
	if target_points < 0:
		raise ValueError(f"Cannot obtain a negative amount ({target_points}) of points.")
	if action not in POINT_AWARDING_ACTIONS:
		raise ValueError(f"The requested action ({action}) cannot provide points. Try one of {POINT_AWARDING_ACTIONS}.")
	return ceil(target_points / ACTIONS[action]['points'])

def bonus_experience(experience):
	return ACTIONS['bonus']['multiplier'] * level(experience)

def rolls_per_kill(points):
	if points < POINTS_REQUIRED:
		return 0
	return min(1 + points / POINTS_REQUIRED, 28)

def kills_for_xp(initial_fm_xp, final_fm_xp, target_points, policy):
	if initial_fm_xp > final_fm_xp:
		raise ValueError(f"Final xp ({final_fm_xp}) cannot exceed initial xp ({initial_fm_xp}).")
	fm = Firemaker(initial_fm_xp, policy)
	kills = 0
	while fm.xp < final_fm_xp:
		fm.kill(target_points)
		kills += 1
	return kills

def hours_for_xp(initial_fm_xp, final_fm_xp, target_points, policy, minutes_per_game_estimate):
	return minutes_per_game_estimate * kills_for_xp(initial_fm_xp, final_fm_xp, target_points, policy) / 60



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Get Wintertodt Information.')
	parser.add_argument('--initial_level', '-i', type=int, nargs='?', default=50, required=False,
	                    help='The initial firemaking level of the player.')
	parser.add_argument('--final_level', '-f', type=int, nargs='?', default=99, required=False,
	                    help='The desired/final firemaking level of the player.')
	parser.add_argument('--game_time', '-t', type=float, nargs='?', default=5, required=False,
	                    help='The time per game.')
	parser.add_argument('--points', '-p', type=int, nargs='?', default=POINTS_REQUIRED, required=False,
	                    help='Number of points per game')
	args = parser.parse_args()

	print(f'Getting {args.points} points per ({args.game_time} minute) game from level {args.initial_level} to {args.final_level} will take:')
	xp_initial, xp_final = experience(args.initial_level), experience(args.final_level)
	kills_kindling = kills_for_xp(xp_initial, xp_final, args.points, Policies.kindling_only)
	kills_roots = kills_for_xp(xp_initial, xp_final, args.points, Policies.roots_only)

	hours_kindling = hours_for_xp(xp_initial, xp_final, args.points, Policies.kindling_only, minutes_per_game_estimate=args.game_time)
	hours_roots = hours_for_xp(xp_initial, xp_final, args.points, Policies.roots_only, minutes_per_game_estimate=args.game_time)
	print(f'\t{kills_kindling} kills using kindling only.')
	print(f'\t{kills_roots} kills using roots only.')
	print(f'\t{hours_kindling:.2f} hours using kindling only.')
	print(f'\t{hours_roots:.2f} hours using roots only.')
	print("Bear in mind that reaching the desired points with only roots is more difficult.")
