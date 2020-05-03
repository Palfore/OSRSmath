""" This module holds the various methods for calculating two functions,
		1) h(n; h_0, m), the expected health of an opponent after n successful hits.
		2) n = hinv(h; h_0, m), the expected number of successful hits for an opponent's health to be h,
	where h_0 is the initial health, and m is the max hit of the attacker.
"""

from math import ceil, floor, log, sqrt
import matplotlib.pyplot as plt
import scipy.optimize
import numpy as np
from scipy.special import beta


class Model:
	def h(self, n, h_0, M):
		raise NotImplementedError

	def hinv(self, h, h_0, M):
		raise NotImplementedError

	def turns_to_kill(self, h_0, M):
		return self.hinv(0, h_0, M)


class Crude(Model):
	def h(self, n, h_0, M):
		return h_0 - n*M/2

	def hinv(self, h, h_0, M):
		return 2 * (h_0 - h) / M


class Average(Model):
	def hinv(self, h, h_0, M):
		assert h == 0
		g = min(M, h_0)
		avg_d = ( g*(g+1) / (h_0*(M+1)) ) * (
			0.5*(M+h_0+1) - (1/3)*(2*g + 1)
		)
		return h_0 / avg_d


class RecursiveApproximation(Model):
	def h(self, n, h_0, M):
		L = 2 * (h_0 / M - 1)
		if n <= L:
			return Crude().h(n, h_0, M)
		else:
			gamma = 0.5/(M + 1)
			return 1 / gamma * (0.5 - gamma)**(2**(n-L))

	def hinv(self, h, h_0, M):
		if h >= M:
			return Crude().hinv(h, h_0, M)
		g = 0.5 / (M + 1)
		L = 2*(h_0 / M - 1)
		return log(log(g*h, .5 - g), 2) + L

	def turns_to_kill(self, h_0, M):
		# Override: The recursive models consider death at h=1
		return self.hinv(1, h_0, M)


class Recursive(Model):
	def h(self, n, h_0, M):
		L = 2 * (h_0 / M - 1)
		if n < L:
			return h_0 - n*M / 2
		else:
			gamma = 0.5/(M + 1)
			return self.f(n-L, gamma, M)

	def hinv(self, h, h_0, M):
		starting_guess = Crude().hinv(h, h_0, M)
		answer = scipy.optimize.newton(
			lambda n: h - self.h(n, h_0, M),
			x0=starting_guess, maxiter=1000
		)
		return answer

	def f(self, n, gamma, f_0):
		if n < 1:
			return 1 / gamma * (gamma*f_0)**(2**n)
		f_n = self.f(n-1, gamma, f_0)
		return gamma*(f_n**2 + f_n)

	def turns_to_kill(self, h_0, M):
		# Override: The recursive models consider death at h=1
		return self.hinv(1, h_0, M)


class MarkovChain(Model):
	@staticmethod
	def n_choose_k(n, k):
		""" Extended to non-integers
			@see https://en.wikipedia.org/wiki/Binomial_coefficient#Two_real_or_complex_valued_arguments """
		return 1 / ( (n + 1) * beta(n - k + 1, k + 1) )

	def hinv(self, h, h_0, M):
		assert h == 0
		# This region suffers from overflow error and other numerical inaccuracies
		# Instead the asymptotic behavior is used.
		if M <= 10 and h_0 > 30:
			return MarkovChainApproximation().hinv(0, h_0, M)
		return sum(
			(
				( ((M+1)/M)**(h_0 - M*i) ) *
				( -1 / (M + 1) )**i *
				MarkovChain.n_choose_k(h_0 - M*i - 1, i)
			) for i in range(0, floor((h_0 - 1) / (M+1)) + 1)
		)


class MarkovChainApproximation(Model):
	def hinv(self, h, h_0, M):
		assert h == 0
		return (2 / M) * (h_0 + (M - 1) / 3)


class Simulation(Model):
	""" Simulates N kills to experimentally approximate the required functions.
		@warning Due to inaccurate negative health handling,
			h(n; h_0, m) should not be trusted when h < m. """
	DEFAULT_N = 10_000

	def __init__(self, N=DEFAULT_N):
		self.N = N

	def h(self, n, h_0, M):
		print("Warning: This method might not be accurate for h(n) < M.")
		h_n = 0
		for i in range(self.N):
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
		assert h <= h_0
		hits = 0
		for i in range(self.N):
			h_i = h_0
			while h_i > h:
				h_i -= np.random.random_integers(0, M)
				hits += 1
		return hits / self.N
