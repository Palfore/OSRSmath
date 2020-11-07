from osrsmath.general.skills import LEVEL_CAP, EXPERIENCE_CAP, level, experience
from bisect import bisect_left
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
		'multiplier': 100
	},
	
}

BURNING_ACTIONS = ['root', 'kindling']
POINT_AWARDING_ACTIONS = [action for action, details in ACTIONS.items() if details['points'] > 0]
REQUIRED_LEVEL = 50
POINTS_REQUIRED = 500

def actions_to_target(action, target_points):
	if target_points < 0:
		raise ValueError(f"Cannot obtain a negative amount ({target_points}) of points.")
	if action not in POINT_AWARDING_ACTIONS:
		raise ValueError(f"The requested action ({action}) cannot provide points. Try one of {POINT_AWARDING_ACTIONS}.")
	return ceil(target_points / ACTIONS[action]['points'])

def bonus_experience(experience):
	return ACTIONS['bonus']['multiplier'] * level(experience)

def crates_per_kill(points):
	if points < POINTS_REQUIRED:
		return 0
	return min(1 + points / POINTS_REQUIRED, 28)

def upper_bound_on_kills(xp_to_gain, target_points):
	# Crude upper bound is obtained by using xp gained from lowest level firemaking possible and no bonus.
	# kindling is also used to reduce xp/kill.
	multiplier = target_points * ACTIONS['kindling']['multiplier'] / ACTIONS['kindling']['points']
	return ceil(xp_to_gain / (multiplier * REQUIRED_LEVEL))

def kills_for_xp(initial_fm_xp, final_fm_xp, target_points, policy):
	max_kills = upper_bound_on_kills(final_fm_xp - initial_fm_xp, target_points)
	fm = Firemaker(initial_fm_xp, policy)
	xp = [fm.E0] + [fm.kill(target_points, 1) for _ in range(max_kills+1)]
	return bisect_left(xp, final_fm_xp, lo=0, hi=max_kills)

def hours_for_xp(initial_fm_xp, final_fm_xp, target_points, policy, minutes_per_game_estimate):
	return minutes_per_game_estimate * kills_for_xp(initial_fm_xp, final_fm_xp, target_points, policy) / 60

class Policies:
	@staticmethod
	def roots_only(firemaker, target_points):
		firemaker.burn('root', n=actions_to_target('root', target_points))

	@staticmethod
	def kindling_only(firemaker, target_points):
		firemaker.burn('kindling', n=actions_to_target('kindling', target_points))

	@staticmethod
	def kindling_till_x(firemaker, target_points, x):
		num_kindling = actions_to_target('kindling', min(x, target_points))
		points_from_kindling = ACTIONS['kindling']['points'] * num_kindling
		points_remaining = max(target_points - points_from_kindling, 0)
		num_roots = actions_to_target('root', points_remaining)
		points_from_roots = ACTIONS['kindling']['points'] * num_roots

		assert points_from_kindling + points_from_roots >= target_points
		firemaker.burn('kindling', num_kindling)
		firemaker.burn('root', num_roots)

	@staticmethod
	def kindling_till_bonus(firemaker, target_points):
		return Policies.kindling_till_x(firemaker, target_points, POINTS_REQUIRED)

class Firemaker:
	def __init__(self, initial_fm_xp, policy=Policies.kindling_till_bonus):
		starting_level = level(initial_fm_xp)
		if starting_level < REQUIRED_LEVEL:
			raise ValueError(f"Wintertodt can only be fought after level {REQUIRED_LEVEL} firemaking, level {starting_level} is too low.")
		
		self.E0 = initial_fm_xp
		self.xp = self.E0
		self.policy = policy
		
	def burn(self, item, n=1):
		if n < 0:
			raise ValueError(f"Cannot perform a negative number ({n}) of actions.")
		if item not in BURNING_ACTIONS:
			raise ValueError(f"Can only burn {BURNING_ACTIONS}, not {item}.")
		for _ in range(n):
			self._gain_xp(ACTIONS[item]['multiplier'] * level(self.xp))
		return self.xp

	def kill(self, target_points=500, k=1):  # By roots only
		if target_points < 0:
			raise ValueError(f"Cannot obtain a negative amount ({target_points}) of points.")
		if k < 0:
			raise ValueError(f"Cannot perform a negative number ({k}) of kills.")

		for _ in range(k):
			self.policy(self, target_points)
			if target_points >= POINTS_REQUIRED:
				self._gain_xp(bonus_experience(self.xp))
		return self.xp

	def _gain_xp(self, xp):
		self.xp = min(round(self.xp + xp, 1), EXPERIENCE_CAP)

if __name__ == '__main__':
	import matplotlib.pyplot as plt
	e50, e99 = experience(50), experience(99)

	## Upper bound on kills required to max, assuming always wins.
	print(kills_for_xp(e50, e99, POINTS_REQUIRED, Policies.kindling_only))
	print(hours_for_xp(e50, e99, POINTS_REQUIRED, Policies.roots_only, minutes_per_game_estimate=5))
	# might also want to plot time to max.
	
	## Plotting kills vs points for 50-99 fm, for different policies
	policies = {
		'Upper Bound': [],
		'Roots': [],
		'Kindling': [],
		'Kind Till Bonus': [],
	}
	for points in list(range(25, 500, 25)) + list(range(500, 1_000, 100)) + list(range(1_000, 13_000, 1000)):
		policies['Upper Bound'].append((points, upper_bound_on_kills(e99 - e50, points)))
		policies['Roots'].append((points, kills_for_xp(e50, e99, points, Policies.roots_only)))
		policies['Kindling'].append((points, kills_for_xp(e50, e99, points, Policies.kindling_only)))
		policies['Kind Till Bonus'].append((points, kills_for_xp(e50, e99, points, Policies.kindling_till_bonus)))
		print(points)

	for policy, data in policies.items():
		plt.plot(*list(zip(*data)), label=f"Policy={policy}")
		plt.scatter(*list(zip(*data)))
	plt.ylabel('Kills Required for 50-99 fm', fontsize=20)
	plt.xlabel('Points', fontsize=20)
	plt.ylim(0, 3000)
	plt.legend(loc='upper right', prop={'size': 14})
	plt.grid('on')
	plt.show()

	## Plotting grand exchange value from 50-99 firemaking, for different base levels & points per game,
	# for a fixed policy.
	# Values obtained from https://oldschool.runescape.wiki/w/Calculator:Wintertodt_supply_crate on 2020-11-04
	crate_values = {
		( 1,  500):  6_799.85,
		( 1,  750):  8_308.68,
		( 1, 1000):  9_817.50,
		# ( 1, 5000): 33_958.73,
		(40,  500): 12_371.24,
		(40,  750): 15_272.91,
		(40, 1000): 18_174.59,
		# (40, 5000): 64_601.38,
		(75,  500): 16_543.89,
		(75,  750): 20_488.73,
		(75, 1000): 24_433.57,
		# (75, 5000): 87_550.98,
		(99,  500): 17_220.78,
		(99,  750): 21_334.85,
		(99, 1000): 25_448.91,
		# (99, 5000): 91_273.88,
	}
	vs_points = {}
	vs_base = {}
	for (base, points), value in crate_values.items():
		kills_required = kills_for_xp(experience(50), experience(99), points, Policies.roots_only)
		# kills_required = kills_for_xp(experience(50), experience(99), points, Policies.kindling_only)
		total = value*crates_per_kill(points)*kills_required
		vs_points.setdefault(base, []).append((points, total/1_000_000))
		vs_base.setdefault(points, []).append((base, total/1_000_000))
	
	fig, (ax1, ax2) = plt.subplots(2, 1)
	for base in reversed(vs_points):
		ax1.plot(*list(zip(*vs_points[base])), label=f"Base={base}")
		ax1.scatter(*list(zip(*vs_points[base])))
	ax1.set_ylabel('Profit [Millions]')
	ax1.set_xlabel('Points per kill')
	ax1.legend(loc='upper right')
	ax1.grid('on')

	for points in reversed(vs_base):
		ax2.plot(*list(zip(*vs_base[points])), label=f"Points={points}")
		ax2.scatter(*list(zip(*vs_base[points])))
	ax2.set_ylabel('Profit [Millions]')
	ax2.set_xlabel('Base level')
	ax2.legend(loc='upper left')
	ax2.grid('on')

	fig.tight_layout()
	plt.show()
