r""" Contains various models dealing with successful hit calculations.

	Each model inherits from `Model` and implements up to three methods:

	* `Model.h`, The expected health of an opponent after \(n\) successful hits.
	* `Model.hinv`, The expected number of successful hits for an opponent's health to be \(h\),
	* `Model.turns_to_kill`, The expected number of successful hits to kill an opponent.

	It is not possible for some models to compute all methods.

	Here is a comparison of the `turn_to_kill` errors from simulation for the different models:
	.. figure:: HEAD/results/part_II/errors.png
"""
# pylint: disable=no-name-in-module  # scipy.special.beta is a C function, so pylint can't find it.
# pylint: disable=misplaced-comparison-constant  # formatting is more clear in this math context.
# pylint: disable=abstract-method  # Not all classes must implement all methods.
# pylint: disable=invalid-name  # Several math-related one letter names are okay.

from math import ceil, floor, log
from scipy.special import beta
import scipy.optimize
import numpy as np

def n_choose_k(n, k):
	""" Extended to non-integers

	See https://en.wikipedia.org/wiki/Binomial_coefficient#Two_real_or_complex_valued_arguments
	"""
	return 1 / ((n + 1) * beta(n - k + 1, k + 1))

def validate(*, n=None, h=None, h_0=None, M=None, a=None, model=None):
	""" Validates any input parameter according to `Model`.

	Must be called with keyword arguments only.
	"""
	tolerance = 1e-12
	if n is not None and not 0 <= n:
		raise ValueError(f"Number of attacks (n) must be non-negative, not {n}.")
	if h is not None and not 0 <= h:
		raise ValueError(f"Final health (h) must be non-negative, not {h}.")
	if h_0 is not None and not 1 <= h_0:
		raise ValueError(f"Initial health (h_0) must be positive, not {h_0}.")
	if M is not None and not 1 <= M:
		raise ValueError(f"Max hit (M) must be positive, not {M}.")
	if a is not None and not tolerance <= a <= 1:
		raise ValueError(f'Accuracy must be in [{tolerance}, 1], not {a}')
	if model is not None:
		if not issubclass(type(model), Model):
			raise ValueError(f'The model must be a Model from: {[cls.__name__ for cls in Model.__subclasses__()]}, not {model}')

class Model:
	""" Computes various quantities given the model's assumptions. """

	def h(self, n: float, h_0: float, M: int):
		r""" Returns the health after \( n \) successful hits.

		Args:
			n: The number of successful attacks \( n \in [0, \infty) \).
			h_0: The initial health of the opponent \( h_0 \in [1, \infty) \).
			M: The max hit of the attacker \( M \in [1, \infty) \).
		Returns:
			The health after \( n \) attacks.
		"""
		raise NotImplementedError()

	def hinv(self, h, h_0, M):
		r""" Calculates the number of successful attacks required to get an opponent to a given health.
		Args:
			h: The final health of the opponent \( h \in [0, h_0) \).
			h_0: The initial health of the opponent \( h_0 \in [1, \infty) \).
			M: The max hit of the attacker \( M \in [1, \infty) \).
		Returns:
			The number of successful attacks to get to \(h\) health.
		"""
		raise NotImplementedError()

	def turns_to_kill(self, h_0, M):
		r""" Calculates the number of turns kill an opponent.

		Args:
			h: The final health of the opponent \( h \in [0, h_0) \).
			h_0: The initial health of the opponent \( h_0 \in [1, \infty) \).
			M: The max hit of the attacker \( M \in [1, \infty) \).
		Returns:
			The number of successful attacks to kill an opponent.
		"""
		return self.hinv(0, h_0, M)


class Crude(Model):
	""" A crude implementation which doesn't consider overkill.

	This is the simplest model.

	Percent error for `turns_to_kill` when compared to simulation:
	.. image:: HEAD/results/part_II/models/Crude.png
	"""
	def h(self, n, h_0, M):
		validate(n=n, h_0=h_0, M=M)
		return h_0 - n*M/2

	def hinv(self, h, h_0, M):
		validate(h=h, h_0=h_0, M=M)
		return 2 * (h_0 - h) / M


class Average(Model):
	""" Considers the piecewise damage as an average for a simplified treatment.

	This average assumes the opponent has all of its health depleted and so only `turns_to_kill` is implemented.
	This model was developed by Nukelawa.

	Percent error for `turns_to_kill` when compared to simulation:
	.. image:: HEAD/results/part_II/models/Average.png
	"""

	def turns_to_kill(self, h_0, M):
		validate(h_0=h_0, M=M)
		g = min(M, h_0)

		coeff = g * (g + 1) / (h_0 * (M + 1))
		left = 0.5 * (M + h_0 + 1)
		right = (1 / 3) * (2 * g + 1)
		avg_d = coeff * (left - right)
		return h_0 / avg_d


class Recursive(Model):
	""" This model considers the piecewise damage as such, providing a recursive solution.
	
	This model was developed by Palfore.

	Percent error for `turns_to_kill` when compared to simulation:
	.. image:: HEAD/results/part_II/models/Recursive.png
	"""
	def h(self, n, h_0, M):
		validate(n=n, h_0=h_0, M=M)
		L = 2 * (h_0 / M - 1)
		if n < L:
			return h_0 - n*M / 2
		gamma = 0.5/(M + 1)
		return self.f(n-L, gamma, M)

	def hinv(self, h, h_0, M):
		validate(h=h, h_0=h_0, M=M)
		starting_guess = Crude().hinv(h, h_0, M)

		def f(n):
			if n < 0:
				return np.inf
			return h - self.h(n, h_0, M)
		answer = scipy.optimize.newton(f, x0=starting_guess, maxiter=1000)
		return answer

	def turns_to_kill(self, h_0, M):
		# Override: The recursive models consider death at h=1
		validate(h_0=h_0, M=M)
		return self.hinv(1, h_0, M)

	def f(self, n, gamma, f_0):
		""" The recursive kernel. """
		if n < 1:
			return 1 / gamma * (gamma*f_0)**(2**n)
		f_n = self.f(n-1, gamma, f_0)
		return gamma*(f_n**2 + f_n)

class RecursiveApproximation(Model):
	""" This model simplifies the `Recursive` model to obtain an analytic expressions.
	
	This model was developed by Palfore.

	Percent error for `turns_to_kill` when compared to simulation:
	.. image:: HEAD/results/part_II/models/RecursiveApproximation.png
	"""

	def h(self, n, h_0, M):
		validate(n=n, h_0=h_0, M=M)
		L = 2 * (h_0 / M - 1)
		if n <= L:
			return Crude().h(n, h_0, M)
		gamma = 0.5/(M + 1)
		return 1 / gamma * (0.5 - gamma)**(2**(n-L))

	def hinv(self, h, h_0, M):
		validate(h=h, h_0=h_0, M=M)
		if h >= M:
			return Crude().hinv(h, h_0, M)
		g = 0.5 / (M + 1)
		L = 2*(h_0 / M - 1)
		return log(log(g*h, .5 - g), 2) + L

	def turns_to_kill(self, h_0, M):
		# Override: The recursive models consider death at h=1
		validate(h_0=h_0, M=M)
		return self.hinv(1, h_0, M)


class MarkovChain(Model):
	""" This model uses a Markov Chain analysis.
	
	This model was developed by Nukelawa.

	Percent error for `turns_to_kill` when compared to simulation:
	.. image:: HEAD/results/part_II/models/MarkovChain.png
	"""

	def turns_to_kill(self, h_0, M):
		validate(h_0=h_0, M=M)
		# pylint: disable=bad-continuation


		# Emperically, catastrophic error occurs above the line defined by two points:
		ax, ay = (0, 0)
		bx, by = (50, 1000)
		m = (by - ay) / (bx - ax)
		b = ay - m*ax
		line = lambda x: m*x + b
		if h_0 > line(M):
		# if M <= 10 and h_0 > 30:
			# Instead the asymptotic behavior is used.
			return MarkovChainApproximation().turns_to_kill(h_0, M)
		return sum(
			(
				(((M + 1) / M)**(h_0 - M*i)) *
				(-1 / (M + 1))**i *
				n_choose_k(h_0 - M*i - 1, i)
			) for i in range(0, floor((h_0 - 1) / (M+1)) + 1)
		)


class MarkovChainApproximation(Model):
	""" This model uses a asymptotic expansion of `MarkovChain` to obtain an analytic expression.
	
	This model was developed by Nukelawa and Corpslayer.

	Percent error for `turns_to_kill` when compared to simulation:
	.. image:: HEAD/results/part_II/models/MarkovChainApproximation.png
	"""

	def turns_to_kill(self, h_0, M):
		validate(h_0=h_0, M=M)
		return (2 / M) * (h_0 + (M - 1) / 3)


class Simulation(Model):
	r""" Simulates \(N\) kills to experimentally approximate the required functions.

		Warning: Due to inaccurate negative health handling, `h` should not be trusted when \(h < m\). """
	DEFAULT_N = 10_000

	def __init__(self, N=DEFAULT_N):
		self.N = N

	def h(self, n, h_0, M):
		validate(n=n, h_0=h_0, M=M)
		print("Warning: This method might not be accurate for h(n) < M.")
		h_n = 0
		for _ in range(self.N):
			h = h_0

			# To handle non-integer n, we only need the average to work out.
			# So if you have n=5.3, do 5 iterations with 30% probability and
			# 6 with 70%.
			fractional = n - floor(n)
			if np.random.uniform(0, 1) < fractional:
				n_fractional = ceil(n)
			else:
				n_fractional = floor(n)

			for _ in range(n_fractional):
				h -= np.random.uniform(0, M)
			h_n += max(h, 0)  # This handling makes this inaccurate, not sure how to fix.
		return h_n / self.N

	def hinv(self, h, h_0, M):
		validate(h=h, h_0=h_0, M=M)
		hits = 0
		for _ in range(self.N):
			h_i = h_0
			while h_i > h:
				h_i -= np.random.random_integers(0, M)
				hits += 1
		return hits / self.N
