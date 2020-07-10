r""" Extends `osrsmath.combat.successful_hits` by considering accuracy \(a\).

	A distinction is made between a 'successful hit' and an 'attempted hit'.
	An attempted hit means an attack has been made (regardless of whether a damage roll
	was made. While a successful hit requires a damage roll. These may be referred to simply
	as a 'hit' when context makes it clear.

	Several parameters are intuitively integers, however floats are often accepted with the
	interpretation of an average.
"""
# pylint: disable=multiple-statements
# pylint: disable=invalid-name  # Several math-related one letter names are okay

import osrsmath.combat.successful_hits as successful_hits

def health_after_attacks(n: float, h_0: float, M: int, a: float, model: successful_hits.Model) -> float:
	r""" Calculates the health of an opponent after a given number of attack attempts.
	Args:
		n: The number of attack attempts \( n \in [0, \infty) \).
		h_0: The initial health of the opponent \( h_0 \in [1, \infty) \).
		M: The max hit of the attacker \( M \in [1, \infty) \).
		a: The accuracy of the attacker \( a \in [0, 1]\).
	 	model: The subclass of `osrsmath.combat.successful_hits.Model` to be used for sucessful hit calculations.
	Returns:
		The health after \( n \) attacks.
	Raises:
		ValueError: If any inputs are out of bounds.
	"""
	successful_hits.validate(n=n, h_0=h_0, M=M, model=model)
	if not 0 <= a <= 1:  # Can actually handle a=0, inverse functions cannot.
		raise ValueError(f'Accuracy must be in [0, 1], not {a}')
	return model.h(n*a, h_0, M)

def attacks_until_health(h: float, h_0: float, M: int, a: float, model: successful_hits.Model) -> float:
	r""" Calculates the number of attack attempts required to get an opponent to a given health.
	Args:
		h: The final health of the opponent \( h \in [0, h_0) \).
		h_0: The initial health of the opponent \( h_0 \in [1, \infty) \).
		M: The max hit of the attacker \( M \in [1, \infty) \).
		a: The accuracy of the attacker \( a \in [0, 1]\).
	 	model: The subclass of `osrsmath.combat.successful_hits.Model` to be used for sucessful hit calculations.
	Returns:
		The number of attacks to get to \(h\) health.
	Raises:
		ValueError: If any inputs are out of bounds.
	"""
	successful_hits.validate(h=h, h_0=h_0, M=M, a=a, model=model)
	return model.hinv(h, h_0, M) / a

def attacks_to_kill(h_0: float, M: float, a: float, model: successful_hits.Model) -> float:
	r""" Calculates the number of turns kill an opponent.

	Note that for some `osrsmath.combat.successful_hits.Model`'s, `attacks_to_kill` is calculated
	differently than `attacks_until_health`, with \(h=0\). For that reason, this function should be used
	if it is the desired quantity.

	Args:
		h: The final health of the opponent \( h \in [0, h_0) \).
		h_0: The initial health of the opponent \( h_0 \in [1, \infty) \).
		M: The max hit of the attacker \( M \in [1, \infty) \).
		a: The accuracy of the attacker \( a \in [0, 1]\).
	 	model: The subclass of `osrsmath.combat.successful_hits.Model` to be used for sucessful hit calculations.
	Returns:
		The number of attacks to kill an opponent.
	Raises:
		ValueError: If any inputs are out of bounds.
	"""
	successful_hits.validate(h_0=h_0, M=M, a=a, model=model)
	return model.turns_to_kill(h_0, M) / a
