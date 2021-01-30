from functools import lru_cache
import matplotlib.pyplot as plt
from pprint import pprint as pp
import numpy as np
from math import floor
import random

class DamageDistribution:
	def __init__(self, c: dict):
		self.c = c
		s = sum(list(self.c.values()))
		if abs(s - 1) >= 1e-8:
			raise ValueError(f"The cumulative distribution sums to {s}, not one.")

		# Fill in missing entries
		for i in range(self.min, self.max):
			self.c[i] = self[i]

		self.c_plus = sum(self[i] for i in range(1, self.max +1))

	def __add__(self, other):
		m = min(self.min, other.min)
		M = max(self.max, other.max)
		assert self.min == 0
		assert other.min == 0

		con = list(np.convolve(
			[self[i] for i in range(m, M+1)],
			[other[i] for i in range(m, M+1)],
		))
		while con[-1] == 0:
			del con[-1]
		return DamageDistribution(dict(enumerate(con)))

	def __getitem__(self, damage):
		return self.c.get(damage, 0)

	def draw(self, amount=None):
		if amount is None:  # None means 1, but return float instead of list
			return self.draw(1)[0]
		return random.choices(list(self.c.keys()), weights=list(self.c.values()), k=amount)
	
	def cdf(self, a=None, b=None):
		if a is None:
			a = self.min
		if b is None:
			b = self.max
		return sum(self[i] for i in range(a, b+1))

	def simulate(self, h, L, f, N=10000):
		# How many times does the opponent have f health on the L'th attack?
		# if f==0, how many times is the opponent killed on the L'th attack?

		count = 0
		for _ in range(N):
			H = h
			
			turns = 0
			while H > 0:
				turns += 1
				H -= self.draw()
				H = max(H, 0)

				if turns == L and H == f:
					count += 1
				elif H < f:
					break

		return count / N

	@lru_cache(maxsize=256)
	def p(self, h, L, f):  # developing function
		if L == 1:
			if f > 0:
				return self[h - f]
			else:
				return sum(self[i] for i in range(h - f, self.max +1))
		if h == 1:
			if f == 1:
				return self[0]**L
			if f == 0:
				return self[0]**(L-1) * self.c_plus

		return (
			self[0] * self.p(h, L-1, f) +
			sum(self[h-i]*self.p(i, L-1, f) for i in range(max(h - self.max, 1, f+1), h-1 +1))
		)
		# return (
		# 	self[0] * self.p(h, L-1, f) +
		# 	sum(self[h-i]*self.p(i, L-1, f) for i in range(max(h - self.max, 1, f+1), h-1))
		# )


	def P(self, h, L, f=0):  # Math solution
		assert f <= h
		if L*self.max < h:
			return 0

		assert list(self.c.keys())[0] == 0, "Assumes self.c starts with 0"
		c_values = list(self.c.values())

		if f >= 1:
			c_values = [c_values[0]] + [(c if (i in range(max(h-self.max, 1, f), h-1 +1)) else 0) for i, c in enumerate(c_values[1:])]

		d = np.polynomial.polynomial.polypow(c_values, L - 1)
		a = lambda j: (
			sum(self[i] for i in range(j, self.max+1)) if f == 0 else (self[j - f])
		)* d[h - j]

		lower = max(1, h + self.max - self.max*L)
		upper = min(h, self.max)
		return sum(a(j) if (h-j) else 0 for j in range(lower, upper +1))

	@property
	def mean(self):
		return np.average(list(self.c.keys()), weights=list(self.c.values()))

	@property
	def max(self):
		return list(self.c.keys())[-1]

	@property
	def min(self):
		return list(self.c.keys())[0]

	def plot(self):
		plt.bar(range(len(self.c)), [100*v for v in list(self.c.values())], align='center')
		plt.axvline(self.mean, color='red')
		# plt.xticks(range(len(self.c)), list(self.c.keys()))
		plt.xlabel('Damage')
		plt.ylabel('Probability')
		return plt

def _join(c_a, c_b, p_b):
	p_a = 1 - p_b
	M = max( max(list(c_a.keys())), max(list(c_b.keys())) )
	c = {}
	for d in range(0, M + 1):
		c[d] = p_a*c_a.get(d, 0) + p_b*c_b.get(d, 0)
	return c

def _transform(distribution, scaling):
	c = {}
	for d, p in distribution.items():
		d = floor(d * scaling)
		c[d] = c.get(d, 0) + p
	return c


def standard(m, a):
	c_plus = a / (m + 1)
	c_0 = 1 - m * c_plus
	c = {0: c_0}
	c.update({
		i: c_plus for i in range(1, m+1)
	})
	return c

def keris(m, a):
	normal = standard(m, a)
	triple = _transform(normal, 3)
	return _join(normal, triple, 1/51)

def verac(m, a):
	normal = standard(m, a)
	perfect = {d+1: p for d, p in standard(m, 1).items()}
	return _join(normal, perfect, 1/4)

def gadderhammer(m, a):
	normal = standard(m, a)
	double = _transform(normal, 2)
	return _join(normal, double, 5/100)

def ahrim(m, a):
	normal = standard(m, a)
	boosted = _transform(normal, 1.3)
	return _join(normal, boosted, 25/100)

def karil(m, a):
	normal = standard(m, a)
	boosted = _transform(normal, 1.5)
	return _join(normal, boosted, 25/100)

def scythe(m, a):
	normal = standard(m, a)
	half = _transform(normal, 0.5)
	quarter = _transform(normal, 0.25)
	return (  # Acts like 3 separate fighters
		DamageDistribution(normal) +
		DamageDistribution(half) +
		DamageDistribution(quarter)
	).c

def opal(m, a, visible_ranged_level, diary=True):
	increase = floor(0.1*visible_ranged_level)
	normal = standard(m, a)
	bolt = standard(m + increase, a)
	return _join(normal, bolt, (5.5/100) if diary else (5/100))

def pearl(m, a, visible_ranged_level, fiery, diary=True):
	if fiery:
		increase = floor(visible_ranged_level/15)
	else:
		increase = floor(visible_ranged_level/20)
	normal = standard(m, a)
	bolt = standard(m + increase, a)
	return _join(normal, bolt, (6.6/100) if diary else (6/100))

def diamond(m, a, diary=True):
	increase = floor(0.15*m)
	normal = standard(m, a)
	bolt = standard(m + increase, 1)
	return _join(normal, bolt, (11/100) if diary else (10/100))

def dragon(m, a, visible_ranged_level, diary=True):
	increase = floor(0.2*visible_ranged_level)
	normal = standard(m, a)
	bolt = standard(m + increase, a)
	return _join(normal, bolt, (6.6/100) if diary else (6/100))

def onyx(m, a, diary=True):
	increase = floor(0.2*m)
	normal = standard(m, a)
	bolt = standard(m + increase, a)
	return _join(normal, bolt, (11/100) if diary else (10/100))

	

def graardor(praying=None):
	# This is a back-of-envelope calculation
	# Maxed with these gear stats:
	# Stab: +308
	# Slash: +303
	# Crush: +315
	# Magic: +97
	# Range: +327

	melee = standard(0 if 'melee' == praying else 60, 0.54)
	ranged = standard(0 if 'ranged' == praying else 35, 0.60)
	combined = _join(melee, ranged, 1/3)
	
	general = DamageDistribution(combined)
	stack = DamageDistribution(standard(15, 0.25))
	will = DamageDistribution(standard(16, 0.30))
	spike = DamageDistribution(standard(21, 0.16))

	return (general + stack + will + spike).c
	

	

if __name__ == '__main__':

	from osrsmath.combat.temp.probabilities import Solution2
	import matplotlib.pyplot as plt
	# c = scythe(10, 0.6)
	# dd = DamageDistribution(c)
	# # dd.plot().show()
	
	# Showing that f=0 both methods agree
	# s2 = Solution2(c)
	# h = 50
	# Ls = list(range(1, 25))
	# plt.plot(Ls, [s2.P(h, L) for L in Ls], label=f"s1")
	# plt.plot(Ls, [dd.P(h, L, 0) for L in Ls], label=f"dd")


	# plt.title("Probability of Dying Against General Graardor after $L$ Attacks.")
	# plt.ylabel("Probability")
	# plt.xlabel("$L$")
	# plt.legend()
	# plt.show()
	# exit()

	# Showing that draw works
	# dd = DamageDistribution(scythe(50, 0.8))
	# plt.plot(list(range(0, dd.max+1)), [dd.c[i] for i in range(0, dd.max+1)], label='Pray=Melee')
	# plt.hist(dd.draw(10000), bins=range(1+dd.max+1), density=True)
	# plt.show()
	# exit()



	Dm = DamageDistribution(graardor('melee'))
	Dr = DamageDistribution(graardor('ranged'))
	Dn = DamageDistribution(graardor(None))

	Dm.plot()
	plt.title('Probability of taking damage against General Graardor if piled')
	plt.xlabel('Damage')
	plt.ylabel('Damage Probability')
	plt.show()

	plt.plot(list(range(1, 100)), [100*Dm.cdf(h) for h in range(1, 100)], label='Pray=Melee')
	plt.plot(list(range(1, 100)), [100*Dr.cdf(h) for h in range(1, 100)], label='Pray=Ranged')
	plt.plot(list(range(1, 100)), [100*Dn.cdf(h) for h in range(1, 100)], label='Pray=None')
	plt.title('Probability of being one-shot by General Graardor if piled\n(for a maxed player in high level gear)')
	plt.xlabel('Player Health')
	plt.ylabel('Death Probability')
	plt.legend()
	plt.show()

	plt.plot(list(range(1, 100)), [100*(Dr.cdf(h) - Dm.cdf(h)) for h in range(1, 100)])
	plt.title('Increase in survival probability between melee and ranged prayer')
	plt.xlabel('Player Health')
	plt.ylabel('Death Probability')
	plt.show()
	