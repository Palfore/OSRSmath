""" This module adds to successful_hits.py by accounting for accuracy, a.
	The method for successful hit calculation can be chosen, and the accuracy
	modifies the answer appropriately. """

import numpy as np

def health_after_attacks(n, h_0, m, a, method):
	""" Calculates the health of an opponent after a certain number of attacks.
		@param n The number of turns to attack for.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param method The calculation method. @see successful_hits.py. """
	assert 0 <= a <= 1
	return method.h(n*a, h_0, m)

def attacks_until_health(h, h_0, m, a, method):
	""" Calculates the number of turns to get an opponent to a given health.
		@param h The final health of the opponent.
		@param h_0 The initial health of the opponent.
		@param m The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param method The calculation method. @see successful_hits.py. """
	tolerance = 1e-12
	assert tolerance <= a <= 1
	if a < tolerance:
		return np.inf
	return method.hinv(h, h_0, m) / a
