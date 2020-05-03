""" This module adds to successful_hits.py by accounting for accuracy, a.
	The model for successful hit calculation can be chosen, and the accuracy
	modifies the answer appropriately. """

import numpy as np

def health_after_attacks(n, h_0, M, a, model):
	""" Calculates the health of an opponent after a certain number of attacks.
		@param n The number of turns to attack for.
		@param h_0 The initial health of the opponent.
		@param M The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param model The successful hits class. @see successful_hits.py. """
	assert 0 <= a <= 1, a
	return model.h(n*a, h_0, M)

def attacks_until_health(h, h_0, M, a, model):
	""" Calculates the number of turns to get an opponent to a given health.
		@param h The final health of the opponent.
		@param h_0 The initial health of the opponent.
		@param M The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param model The successful hits class. @see successful_hits.py. """
	tolerance = 1e-12
	assert tolerance <= a <= 1, a
	return model.hinv(h, h_0, M) / a

def attacks_to_kill(h_0, M, a, model):
	""" Calculates the number of turns to get an opponent to a given health.
		@param h_0 The initial health of the opponent.
		@param M The max hit of the attacker.
		@param a The accuracy of the attacker.
		@param model The successful hits class. @see successful_hits.py. """
	tolerance = 1e-12
	assert tolerance <= a <= 1, a
	return model.turns_to_kill(h_0, M) / a
