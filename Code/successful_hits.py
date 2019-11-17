""" This module holds the various methods for calculating two functions,
		1) h(n; h_0, m), the expected health of an opponent after n successful hits.
		2) n = hinv(h; h_0, m), the expected number of successful hits for an opponent's health to be h,
	where h_0 is the initial health, and m is the max hit of the attacker.

	For very low m, and very high h_0 the Recursive method exceeds the recursion limit.
	Other methods agree the most with this one in this domain, so it's advised to use those
	instead. """

from math import ceil, floor, log
import matplotlib.pyplot as plt
import scipy.optimize
import numpy as np

class Crude:
	""" This method does not consider overkill, and treats
		each hit as uniformly distributed between [0, m]. """

	def h(self, n, h_0, m):
		return h_0 - n*m/2

	def hinv(self, h, h_0, m):
		assert h <= h_0
		return 2 * (h_0 - h) / m

class Approximate:
	""" This method considers overkill, but ignores a linear term in
		the recursive equation to allow for an approximate analytic form. """
	def h(self, n, h_0, m):
		L = 2 * (h_0 / m - 1)
		if n <= L:
			return h_0 - n*m / 2
		else:
			gamma = 0.5/(m + 1)
			return 1 / gamma * (0.5 - gamma)**(2**(n-L))

	def hinv(self, h, h_0, m):
		assert h <= h_0
		g = 0.5 / (m + 1)
		L = 2*(h_0 / m - 1)
		h_L = h_0 - L*m/2
		log_g = np.log(g)
		log_gh = np.log(g*h_L)
		return np.log(log_g / log_gh) + L

class Recursive:
	""" This is the most accurate method, which includes all terms, but approximates
		the initial health for the second case (h < m) to accommodate non-integers. """
	def h(self, n, h_0, m):
		L = 2 * (h_0 / m - 1)
		if n <= L:
			return h_0 - n*m / 2
		else:
			gamma = 0.5/(m + 1)
			return Recursive.f(n-L, gamma, m)

	def hinv(self, h, h_0, m):
		assert h <= h_0
		starting_guess = Crude().hinv(h, h_0, m)
		return scipy.optimize.newton(
			lambda n: abs(h - self.h(n, h_0, m)),
			x0=starting_guess, maxiter=100
		)

	@staticmethod
	def f(n, gamma, f_0):
		''' Satisfies f(n) = gamma( f(n-1)^2 + f(n-1) ), subject to f(n) = f_0 '''
		if n < 1:
			return 1 / gamma * (gamma*f_0)**(2**n)
		f_n = Recursive.f(n-1, gamma, f_0)
		return gamma*(f_n**2 + f_n)

class Experimental:
	""" Simulates N kills to experimentally approximate the required functions.
		@warning Due to inaccurate negative health handling,
			h(n; h_0, m) should not be trusted when h < m. """
	DEFAULT_N = 100_000

	def __init__(self, N=DEFAULT_N):
		self.N = N

	def h(self, n, h_0, m):
		print("Warning: This method is not accurate, and should not be trusted for h(n) < m.")
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
			c = 0
			h = h_0
			while h >= 1:
				h -= np.random.uniform(0, m)
				c += 1
			hits += c
		return hits / self.N

if __name__ == '__main__':
	from mpl_toolkits.mplot3d import Axes3D
	from matplotlib import cm
	import sys

	# sys.setrecursionlimit(5000)
	m_min, m_max = (10, 110)
	h_min, h_max = (10, 255)

	fig = plt.figure()
	ax = fig.gca(projection='3d')
	x = np.array(range(m_min, m_max+1))
	y = np.array(range(h_min, h_max+1))
	X, Y = np.meshgrid(x, y)

	# ax.set_zlabel("Turns to kill")
	# Z = np.array([np.array([Experimental().hinv(1, h, m) for m in x]) for h in y])
	# ax.plot_wireframe(X, Y, Z, color='red', label="Experimental")

	# Z = np.array([np.array([Recursive().hinv(1, h, m) for m in x]) for h in y])
	# ax.plot_wireframe(X, Y, Z, color='black', label="Recursive")

	# Z = np.array([np.array([Crude().hinv(1, h, m) for m in x]) for h in y])
	# ax.plot_wireframe(X, Y, Z, color='green', label="Crude")


	ax.set_zlabel("Percent Error")
	Z = np.array([np.array([(abs(1 - Recursive().hinv(1, h, m) / Experimental().hinv(1, h, m)))*100 for m in x]) for h in y])
	surf = ax.plot_wireframe(X, Y, Z, color='black', linewidth=0.3, label="Crude Error")

	Z = np.array([np.array([(abs(1 - 0.5*(Recursive().hinv(1, h, m) + Crude().hinv(1, h, m)) / Experimental().hinv(1, h, m)))*100 for m in x]) for h in y])
	surf = ax.plot_wireframe(X, Y, Z, color='red', linewidth=0.3, label="Average Error")

	plt.xlabel("Max Hit")
	plt.ylabel("Initial Health")
	plt.legend()
	ax.view_init(-57, 20)
	plt.show()

	exit()
	h_0 = 200
	m = 30
