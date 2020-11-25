""" Contains an implementation for some fighting probability equations from Appendix C.

This includes the probability of a fight ending after L attacks, and the probability of 
different outcomes (win/lose/draw) for a fight. In addition, there is an interactive 
display that allows a user to plot the latter equations under different parameters.

There are two sets of widgets to interact with:
    1) Radio Buttons: Select which variable to plot along the x axis.
    2) Sliders: Fix the values of the other parameters.
                The currently plotted variable is ignored.
                Each change takes about 1-2 seconds.
                NUM_PROCESSES can be updated depending on computer resources.
Calculations are relatively slow so (before proper optimizations) lru_cache 
is used. Several of these *may* be redundant. 
"""

NUM_PROCESSES = 12

from collections import namedtuple
from functools import lru_cache
from random import randint, uniform
from math import floor, comb
import numpy as np

class Solution:
	def __init__(self, acc, m):
		self.acc = acc
		self.m = m
		self.c0 = self.acc / (self.m + 1)
		self.c1 = self.m * self.c0
		self.c2 = 1 - self.c1
		self.c3 = self.c0 + self.c2

	def G(self, h, i, p):
		return (self.c0 / self.c2)**p * sum(
			(-1)**l * comb(p, l) * comb(h - i - self.m*l - 1, h - i - self.m*l - p)
			for l in range(0, min(floor((h - i - p) / self.m), p)+1)
		)

	def H(self, h, i, L):
		return self.c0 * self.c2**(L - 1) * (self.m - i + 1) * sum(
			comb(L-1, p) * self.G(h, i, p)
			for p in range(1, min(h - i, L - 1) + 1)
		)

	@lru_cache(maxsize=256)
	def P(self, h, L):
		return self.c0 * self.c2**(L - 1)*max(self.m - h + 1, 0) + sum(
			self.H(h, i, L)
			for i in range(1, min(h, self.m)+1)
		)

	@lru_cache(maxsize=256)
	def infty_sumP(self, h, b):
		A = self.c0 * max(self.m - h + 1, 0) * self.c2**(b - 1) / (1 - self.c2)
		s = 0
		for i in range(1, min(self.m, h)+1):
			C_i = self.c0 * (self.m - i + 1)
			for L in range(b, h - i +1):
				for p in range(1, L - 1 +1):
					s += C_i * self.c2**(L-1) * comb(L - 1, p) * self.G(h, i, p)
		
			for p in range(1, h - i +1):
				S = C_i * self.c2**p / (1 - self.c2)**(p + 1)
				for j in range(1, max(b - 1, h - i) - 1 +1):
					S -= C_i * self.c2**j * comb(j, p)
				s += self.G(h, i, p) * S
		return A + s

class Duel:
	INFINITY = 100  # The outer sum doesn't have an analytic form (yet at least) so this crude cutoff is being used.
	                # For long fights, this might cause issues.
	                # In future, a proper bound should be computed or an analytic form should be used.

	def __init__(self, a, m, h, A, M, H):
		Fighter = namedtuple('Fighter', ['a', 'm', 'h', 'solution'])
		self.player = Fighter(a, m, h, Solution(a, m))
		self.opponent = Fighter(A, M, H, Solution(A, M))

	def get_simulation_probabilities(self):
		N = 100
		wins, draws, loses = 0, 0, 0
		for fight in range(N):
			h = self.player.h
			H = self.opponent.h
			while H > 0 and h > 0:
				H -= int(uniform(0, 1) <   self.player.a) * randint(0, self.player.m)
				h -= int(uniform(0, 1) < self.opponent.a) * randint(0, self.opponent.m)
				H = max(H, 0)
				h = max(h, 0)
			if H == 0 and h == 0:
				draws += 1
			elif H == 0:
				wins += 1
			elif h == 0:
				loses += 1
			else:
				raise
		return wins / N, loses / N, draws / N

	def P_win(self):
		return sum(self.player.solution.P(self.opponent.h, L) * self.opponent.solution.infty_sumP(self.player.h, L+1)
					for L in range(1, self.INFINITY))

	def P_lose(self):
		return sum(self.opponent.solution.P(self.player.h, L) * self.player.solution.infty_sumP(self.opponent.h, L+1)
					for L in range(1, self.INFINITY))

	def P_draw(self):
		return sum(self.opponent.solution.P(self.player.h, L) * self.player.solution.P(self.opponent.h, L) for L in range(1, self.INFINITY))

	def get_probabilities(self):
		w, d = self.P_win(), self.P_draw()
		l = self.P_lose()
		# l = 1 - w - d  # This can be used to speed things up, but its less safe
		if abs(w + l + d - 1) >= 1e-8:
			print(f'Warning: probabilities add to {w+l+d} not 1.')
		return w, l, d

if __name__ == '__main__':
	from matplotlib.widgets import Slider, RadioButtons
	import numpy as np
	import matplotlib.pyplot as plt
	from multiprocessing import Pool

	@lru_cache(maxsize=256)
	def f(x, selector=0):
		a, m, h, A, M, H = x
		m, h = int(m), int(h)
		M, H = int(M), int(H)
		x = a, m, h, A, M, H
		probabilities = Duel(*x).get_probabilities()[selector]
		return probabilities

	@lru_cache(maxsize=256)
	def g(x, selector=0):
		a, m, h, A, M, H = x
		m, h = int(m), int(h)
		M, H = int(M), int(H)
		x = a, m, h, A, M, H
		probabilities = Duel(*x).get_simulation_probabilities()[selector]
		return probabilities

	# Multiprocessing can't use lambdas
	def WIN(x):
		return f(x, 0)

	def LOSE(x):
		return f(x, 1)

	def DRAW(x):
		return f(x, 2)

	def SIM_WIN(x):
		return g(x, 0)

	def SIM_LOSE(x):
		return g(x, 1)

	def SIM_DRAW(x):
		return g(x, 2)

	fig = plt.figure(figsize=(8,3))
	plt_axes = plt.axes([0.1, 0.4, 0.8, 0.55])

	checkbox = RadioButtons(
		ax=plt.axes([0, 0.0, 0.1, 0.3]),
		labels=['a', 'm', 'h', 'A', 'M', 'H'],
	)
	a = Slider(
		ax=plt.axes([0.1, 0.005, 0.8, 0.03]),
		label='a',
		valmin=0.01,
		valmax=1,
		valinit=1.0,
	)
	m = Slider(
		ax=plt.axes([0.1, 0.05, 0.8, 0.03]),
		label='m',
		valmin=1,
		valmax=30,
		valinit=10,
	)
	h = Slider(
		ax=plt.axes([0.1, 0.1, 0.8, 0.03]),
		label='h',
		valmin=1,
		valmax=30,
		valinit=20,
	)
	A = Slider(
		ax=plt.axes([0.1, 0.15, 0.8, 0.03]),
		label='A',
		valmin=0.01,
		valmax=1,
		valinit=0.55,
	)
	M = Slider(
		ax=plt.axes([0.1, 0.20, 0.8, 0.03]),
		label='M',
		valmin=1,
		valmax=30,
		valinit=5,
	)
	H = Slider(
		ax=plt.axes([0.1, 0.25, 0.8, 0.03]),
		label='H',
		valmin=1,
		valmax=30,
		valinit=25,
	)

	plt.axes(plt_axes)
	plt.title('Probability of Fight Outcomes')
	plt.ylabel('Probability of Event')
	plt.xlabel('Player Accuracy')
	var = a
	x = np.linspace(var.valmin, var.valmax, 40)
	y = np.linspace(var.valmin, var.valmax, 40)
	win_plot, = plt.plot(x, y, 'g')
	lose_plot, = plt.plot(x, y, 'r')
	draw_plot, = plt.plot(x, y, 'b')
	# sim_win_plot, = plt.plot(x, y, 'o')
	# sim_lose_plot, = plt.plot(x, y, 'r')
	# sim_draw_plot, = plt.plot(x, y, 'b')

	def update(_):
		var = {'a': a, 'm': m, 'h': h, 'A': A, 'M': M, 'H': H}[checkbox.value_selected]
		plt.xlabel({
			'a': 'Player Accuracy',
			'm': 'Player Max Hit',
			'h': 'Player Health',
			'A': 'Opponent Accuracy',
			'M': 'Opponent Max Hit',
			'H': 'Opponent Health',
		}[checkbox.value_selected])
		
		X = np.linspace(var.valmin, var.valmax, 40)
		if checkbox.value_selected in ['m', 'h', 'M', 'H']:
			X = np.linspace(var.valmin, var.valmax, var.valmax - var.valmin + 1)


		values = {symbol: [symbol.val]*len(X) for symbol in [a, m, h, A, M, H]}
		values[var] = X
		print('Updating')
		with Pool(processes=NUM_PROCESSES) as pool:
			print('Win')
			win_plot.set_data(
				X,
				np.array(pool.map(WIN, list(zip(
					*list(values.values())
				))))
			)
			print('Lose')
			lose_plot.set_data(
				X,
				np.array(pool.map(LOSE, list(zip(
					*list(values.values())
				))))
			)
			print('Draw')
			draw_plot.set_data(
				X,
				np.array(pool.map(DRAW, list(zip(
					*list(values.values())
				))))
			)
			# sim_win_plot.set_data(
			# 	X,
			# 	np.array(pool.map(SIM_WIN, list(zip(
			# 		*list(values.values())
			# 	))))
			# )
			# sim_lose_plot.set_data(
			# 	X,
			# 	np.array(pool.map(SIM_LOSE, list(zip(
			# 		*list(values.values())
			# 	))))
			# )
			# sim_draw_plot.set_data(
			# 	X,
			# 	np.array(pool.map(SIM_DRAW, list(zip(
			# 		*list(values.values())
			# 	))))
			# )
		print('Finished')
		plt.xlim(var.valmin, var.valmax)
		fig.canvas.draw_idle()

	checkbox.on_clicked(update)
	a.on_changed(update)
	m.on_changed(update)
	h.on_changed(update)
	A.on_changed(update)
	M.on_changed(update)
	H.on_changed(update)
	update(None)
	text_lables = {label.get_text(): i for i, label in enumerate(checkbox.labels)}
	checkbox.set_active(text_lables['m'])
	plt.show()