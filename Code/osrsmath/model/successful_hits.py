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

class Crude:
	def h(self, n, h_0, m):
		return h_0 - n*m/2

	def hinv(self, h, h_0, m):
		return 2 * (h_0 - h) / m

class Average:
	def h(self, n, h_0, m):
		raise NotImplementedError

	def hinv(self, h, h_0, m):
		assert h == 0
		g = min(m, h_0)
		avg_d = ( g*(g+1) / (h_0*(m+1)) ) * (
			0.5*(m+h_0+1) - (1/3)*(2*g + 1)
		)
		return h_0 / avg_d

class RecursiveApproximate:
	def h(self, n, h_0, m):
		L = 2 * (h_0 / m - 1)
		if n <= L:
			return h_0 - n*m / 2
		else:
			gamma = 0.5/(m + 1)
			return 1 / gamma * (0.5 - gamma)**(2**(n-L))

	def hinv(self, h, h_0, m):
		raise NotImplementedError("Not sure the log is correct")
		assert h <= h_0
		g = 0.5 / (m + 1)
		L = 2*(h_0 / m - 1)
		h_L = h_0 - L*m/2
		log_g = np.log(g)
		log_gh = np.log(g*h_L)
		return np.log(log_g / log_gh) + L

class Recursive:
	def h(self, n, h_0, m):
		L = 2 * (h_0 / m - 1)
		if n <= L:
			return h_0 - n*m / 2
		else:
			gamma = 0.5/(m + 1)
			return self.f(n-L, gamma, m)

	def hinv(self, h, h_0, m):
		assert h <= h_0
		starting_guess = Crude().hinv(h, h_0, m)
		answer = scipy.optimize.newton(
			lambda n: h - self.h(n, h_0, m),
			x0=starting_guess, maxiter=1000
		)
		return answer

	def f(self, n, gamma, f_0):
		if n < 1:
			return 1 / gamma * (gamma*f_0)**(2**n)
		f_n = self.f(n-1, gamma, f_0)
		return gamma*(f_n**2 + f_n)

class Simulation:
	""" Simulates N kills to experimentally approximate the required functions.
		@warning Due to inaccurate negative health handling,
			h(n; h_0, m) should not be trusted when h < m. """
	DEFAULT_N = 10_000

	def __init__(self, N=DEFAULT_N):
		self.N = N

	def h(self, n, h_0, m):
		print("Warning: This method might not be accurate for h(n) < m.")
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
				h -= np.random.uniform(0, m)
			h_n += max(h, 0)  # This handling makes this inaccurate, not sure how to fix.
		return h_n / self.N

	def hinv(self, h, h_0, m):
		assert h <= h_0
		hits = 0
		for i in range(self.N):
			h_i = h_0
			while h_i > h:
				h_i -= np.random.random_integers(0, m)
				hits += 1
		return hits / self.N


