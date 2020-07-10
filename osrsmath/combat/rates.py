""" This module adds to hits.py by accounting for weapon speed, s.
	The model for successful hit calculation can be chosen, and the
	weapon speed modifies the calculation appropriately. """

import osrsmath.combat.hits as hits

def health_after_time(t, h_0, m, a, T_A, model):
	""" Returns the health of the opponent after a given time (in seconds).
		@param t The time (in seconds) to attack for.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param T_A The attack interval of the attacker.
		@param model The calculation model. @see successful_hits.py. """
	return hits.health_after_attacks(t/T_A, h_0, m, a, model)

def time_until_health(h, h_0, m, a, T_A, model):
	""" Returns the time (in seconds) to bring an opponent to a given health.
		@param t The time (in seconds) to attack for.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param T_A The attack interval of the attacker.
		@param model The calculation model. @see successful_hits.py. """
	return hits.attacks_until_health(h, h_0, m, a, model) * T_A

def time_to_kill(h_0, m, a, T_A, model):
	""" Returns the time (in seconds) to kill an opponent.
		@param t The time (in seconds) to attack for.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param T_A The attack interval of the attacker.
		@param model The calculation model. @see successful_hits.py. """
	return hits.attacks_to_kill(h_0, m, a, model) * T_A

def experience_per_hour(h_0, m, a, T_A, e, model):
	""" Returns the experience per hour assuming continuous fighting.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param T_A The attack interval of the attacker.
		@param e The experience awarded per damage.
		@param model The calculation model. @see successful_hits.py. """
	return e * h_0 / time_to_kill(h_0, m, a, T_A, model) * 60*60

def hours_until_experience(E, h_0, m, a, T_A, e, model):
	""" Returns the number of hours
		@param E The experience desired.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param T_A The attack interval of the attacker.
		@param e The experience awarded per damage.
		@param model The calculation model. @see successful_hits.py.
		@warning Note these are expected calculation, so only large values of E
			will be accurate. But then the player should note that if they level up
			these values will change. """
	return E / experience_per_hour(h_0, m, a, T_A, e, model)
