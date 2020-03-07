""" This module adds to hits.py by accounting for weapon speed, s.
	The method for successful hit calculation can be chosen, and the
	weapon speed modifies the calculation appropriately. """

import osrsmath.model.hits as hits

def health_at_time(t, h_0, m, a, s, method):
	""" Returns the health of the opponent after a given time (in seconds).
		@param t The time (in seconds) to attack for.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param s The attack speed of the attacker.
		@param method The calculation method. @see successful_hits.py. """
	return hits.health_after_attacks(t*s, h_0, m, a, method)

def time_until_health(h, h_0, m, a, s, method):
	""" Returns the time (in seconds) to bring an opponent to a given health.
		@param t The time (in seconds) to attack for.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param s The attack speed of the attacker.
		@param method The calculation method. @see successful_hits.py. """
	return hits.attacks_until_health(h, h_0, m, a, method) / s

def experience_per_hour(h_0, m, a, s, e, method):
	""" Returns the experience per hour during a fight.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param s The attack speed of the attacker.
		@param e The experience awarded per damage.
		@param method The calculation method. @see successful_hits.py. """
	return e * h_0 / time_until_health(1, h_0, m, a, s, method) * 60*60

def time_until_experience(E, h_0, m, a, s, e, method):
	""" Returns the experience per hour during a fight.
		@param E The experience desired.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param s The attack speed of the attacker.
		@param e The experience awarded per damage.
		@param method The calculation method. @see successful_hits.py.
		@warning Note these are expected calculation, so only large values of E
			will be accurate. But then the player should note that if they level up
			these values will change. """
	return E * time_until_health(1, h_0, m, a, s, method) / (e * h_0 * 60*60)

if __name__ == '__main__':
	import successful_hits

	opponents = {  # Easy Mode
		'Count Draynor': {'hp': 35, 'acc': 0.9086},
		'King Roland': {'hp': 60, 'acc': 0.9100},
		'Me': {'hp': 45, 'acc': 0.8086},
		'Tree Spirit': {'hp': 85, 'acc': 0.7948},
		'Khazard Warlord': {'hp': 170, 'acc': 0.7948},
	}

	# opponents = {  # Hard mode
	# 	'Count Draynor': {'hp': 210, 'acc': 0.9086},
	# 	'King Roland': {'hp': 150, 'acc': 0.9100},
	# 	'Me': {'hp': 135, 'acc': 0.8086},
	# 	'Tree Spirit': {'hp': 187, 'acc': 0.7948},
	# 	'Khazard Warlord': {'hp': 255, 'acc': 0.7948},
	# }

	def average_exp(method, printing):
		if printing:
			print()
		E_avg_r = 0
		for name, stats in opponents.items():
			E = experience_per_hour(stats['hp'], 26, stats['acc'], 1.0/2.4, 4, getattr(successful_hits, method)())
			if printing:
				print(name, E)
			E_avg_r += E
		E_avg_r /= len(opponents)
		return E_avg_r


	for method in ['Recursive', 'Crude', 'Simulation']:
		print(f"Average {method}:", average_exp(method, True))
