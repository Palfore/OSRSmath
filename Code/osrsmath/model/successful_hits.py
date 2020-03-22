""" This module holds the various methods for calculating two functions,
		1) h(n; h_0, m), the expected health of an opponent after n successful hits.
		2) n = hinv(h; h_0, m), the expected number of successful hits for an opponent's health to be h,
	where h_0 is the initial health, and m is the max hit of the attacker.

	For very low m, and very high h_0 the Recursive method exceeds the recursion limit.
	Other methods agree the most with this one in this domain, so it's advised to use those
	instead.

	@todo: Determine and add bitter's equation.
"""

from math import ceil, floor, log, sqrt
import matplotlib.pyplot as plt
import scipy.optimize
import numpy as np

class Crude:
	""" This method does not consider overkill, and treats
		each hit as uniformly distributed between [0, m]. """

	def h(self, n, h_0, m):
		return h_0 - n*m/2

	def hinv(self, h, h_0, m):
		return 2 * (h_0 - h) / m

class Average:
	# Nukelawe Contribution: https://imgur.com/aykEahg
	# BitterKoekje: https://docs.google.com/spreadsheets/d/1xCztykHho5R2Ce_vAGowLCja8HFMHJrjqHok9r2Q13Y/edit#gid=124277451
	# (I think) The issue with this calculation is that it doesn't consider that the
	# ``average damage' occurs in different amounts. So the experience rates can't be treated using this average.

	@staticmethod
	def expected_kill_time(h_0, m):
		# Only considers h_0->0.
		if h_0 < 1e-8:
			return 0
		g = min(m, h_0)
		avg_d = ( g*(g+1) / (h_0*(m+1)) ) * (
			0.5*(m+h_0+1) - (1/3)*(2*g + 1)
		)
		return h_0 / avg_d

	def h(self, n, h_0, m):
		# raise NotImplementedError
		if h_0 <= m:
			a = -n/3
			b = m*n - 2*(m + 1)
			c = n*(m + 1/3)
		else:
			a = -1
			b = m*n/2
			c = (1 - m) * m*n/6

		delta = (b**2) - (4*a*c)
		solution1 = (-b - sqrt(delta)) / (2*a)
		solution2 = (-b + sqrt(delta)) / (2*a)
		print('>>>', solution1, solution2)
		return h_0 - solution1  # not sure if should use 1 or 2

	def hinv(self, h, h_0, m):
		return self.expected_kill_time(h_0, m) - self.expected_kill_time(h, m)

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
		raise NotImplementedError("Not sure the log is correct")
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
	def __init__(self):
		self.num_calls = 0

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
		try:
			answer= scipy.optimize.newton(
				lambda n: h - self.h(n, h_0, m),
				x0=starting_guess, maxiter=1000
			)
			# print(self.num_calls, h, h_0, m)
			return answer
		except Exception as e:
			print(e, h, h_0, m)
			# raise e
			return 0

	def f(self, n, gamma, f_0):
		''' Satisfies f(n) = gamma( f(n-1)^2 + f(n-1) ), subject to f(n) = f_0 '''
		self.num_calls += 1
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
		if m == 1:  # Debugging
			print(f"h_0={h_0}")
		assert h <= h_0
		hits = 0
		for i in range(self.N):
			h_i = h_0
			while h_i > h:
				h_i -= np.random.random_integers(0, m)
				hits += 1
		return hits / self.N




## Multi-processing boiler plate
from multiprocessing import Pool
_func = None
def worker_init(func):
  global _func
  _func = func
def worker(x):
  return _func(x)
def xmap(func, iterable, processes=None):
  with Pool(processes, initializer=worker_init, initargs=(func,)) as p:
    return p.map(worker, iterable)


if __name__ == '__main__':
	from pprint import pprint
	import inspect
	import os
	import json

	N = 1_00_000
	dataset_name = f"../Data/simulations/simulation.{N}.dat"
	if not os.path.exists(dataset_name):
		print("Creating Dataset")
		dataset = {
			"N": N,
			"source": inspect.getsource(Simulation(N).hinv),
			"data": {
				str(h): {
					str(m): hinv  for m, hinv in xmap(lambda m: (str(m), Simulation(N).hinv(0, h, m)), x, processes=12)
				} for h in y
			}
		}
		print("Saving Dataset")
		with open(dataset_name, 'w') as f:
			json.dump(dataset, f)
	print("Loading in Dataset")
	sim = json.load(open(dataset_name))['data']


	##############################################
	from mpl_toolkits.mplot3d import Axes3D
	from matplotlib import cm
	import sys

	m_min, m_max = (1, 110)
	h_min, h_max = (1, 255)
	x = np.array(range(m_min, m_max+1))
	y = np.array(range(h_min, h_max+1))
	X, Y = np.meshgrid(x, y)

	# https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary

	colors = {
		"Crude": "red",
		"Average": "orange",
		"Recursive": "black",
		"MarkovChainApprox": "green",
		"MarkovChain": "blue",
	}
	import operator
	Z = np.array([np.array([
		list(colors).index(
			min({
				n: abs(1 - getattr(sys.modules[__name__], n)().hinv(0.5 if n == "Recursive" else 0, h, m) / sim[str(h)][str(m)] ) for n in colors
			}.items(), key=operator.itemgetter(1))[0]
		)
	for m in x]) for h in y])

	import matplotlib as mpl

	ax = plt.gca()
	cmap = mpl.colors.ListedColormap(list(colors.values()))

	import matplotlib.colors as clrs
	boundaries = [-0.5] + [list(colors).index(c) + 0.5 for c in colors]
	norm = clrs.BoundaryNorm(boundaries, cmap.N, clip=True)

	plt.pcolor(Z, cmap=cmap, norm=norm)
	cb = plt.colorbar()


	cb.set_ticks([list(colors).index(c) for c in colors])
	cb.set_ticklabels(list(colors.keys()))

	plt.ylabel("$h_0$")
	plt.xlabel("M")
	plt.show()
	exit()


	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.set_zlabel("Percent Error")

	# ax.set_zlabel("Turns to kill")
	# Z = np.array([np.array([Simulation().hinv(1, h, m) for m in x]) for h in y])
	# ax.plot_wireframe(X, Y, Z, color='red', label="Simulation")

	def plot_error(label, color, inverse):
		""" inverse: hinv(h, m) """
		print(label)
		Z = np.array([np.array([(abs(1 - inverse(h, m) / sim[str(h)][str(m)] ))*100 for m in x]) for h in y])
		surf = ax.plot_wireframe(X, Y, Z, color=color, linewidth=0.9, label=f"{label}")
		print(np.average(Z), np.var(Z), np.max(Z), np.min(Z))

	plot_error("Recursive", "black", lambda h, m: Recursive().hinv(1, h, m))
	# plot_error("Crude", "red", lambda h, m: Crude().hinv(0, h, m))
	plot_error("Average", "orange", lambda h, m: Average().hinv(0, h, m))
	plot_error("MarkovChain", "blue", lambda h, m: MarkovChain().hinv(0, h, m))
	plot_error("MarkovChainApprox", "green", lambda h, m: MarkovChainApprox().hinv(0, h, m))

	plt.xlabel("Max Hit")
	plt.ylabel("Initial Health")
	plt.legend()
	ax.view_init(-57, 20)
	plt.show()

