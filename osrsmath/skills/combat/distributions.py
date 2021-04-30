from functools import lru_cache
import matplotlib.pyplot as plt
from pprint import pprint as pp
import numpy as np
from math import floor
import random
import osrsmath.skills.combat.accuracy as accuracy

class KillDistribution:
	def __init__(self, damage_distribution, opponent_health, f=0, tol=1e-6):
		self.dd = damage_distribution
		self.h = opponent_health
		self.tol = tol
		self.f = f  # Final health
		assert f == 0, "Non-zero final health is not yet handled."

		self.fastest = int(np.ceil( (self.h - self.f) / self.dd.max)) # Earliest L to bring an opponent to f health
		self.cutoff = self.quantile(p=1)  # L corresponding to 1-tol cdf (used for summing to infinity)

	@lru_cache(maxsize=256)
	def pmf(self, L, f=0):
		""" Returns the probability mass function. """
		# These is possibly an issue with using other distributions (keris, etc)
		# I'm not yet sure exactly what's causing issues, but it's likely something like 0 probabilities or non-sequential
		# values. A good place to start is investigating polypow. 
		# print(lower, upper, h, self.dd.max, -self.dd.max*L, L)
		assert list(self.dd.c.keys()) == list(range(self.dd.min, self.dd.max+1)), "Assumes sequential values"
		assert f == 0, "Non-zero final health is not yet handled."
		assert f <= self.h
		if L*self.dd.max < self.h:
			return 0

		assert list(self.dd.c.keys())[0] == 0, "Assumes self.c starts with 0"
		c_values = list(self.dd.c.values())

		if f >= 1:
			c_values = [c_values[0]] + [(c if (i in range(max(self.h-self.dd.max, 1, f), self.h-1 +1)) else 0) for i, c in enumerate(c_values[1:])]

		d = np.polynomial.polynomial.polypow(c_values, L - 1)
		a = lambda j: (
			sum(self.dd[i] for i in range(j, self.dd.max+1)) if f == 0 else (self.dd[j - f])
		)* d[self.h - j]

		lower = max(1, self.h + self.dd.max - self.dd.max*L)
		upper = min(self.h, self.dd.max)
		return sum(a(j) if (self.h-j) else 0 for j in range(lower, upper +1)) 

	def quantile(self, p):
		if not (0 <= p <= 1):
			raise ValueError(f"p must be between 0 and 1, not {p}.")

		s, L = 0, self.fastest
		while s < p - self.tol:
			s += self.pmf(L, self.f)
			L += 1
		return L
		

class DamageDistribution:
	def __init__(self, c: dict):
		self.c = c
		s = sum(list(self.c.values()))
		if abs(s - 1) >= 1e-8:
			raise ValueError(f"The distribution sums to {s}, not one.")

		assert self.min == 0  # No negatives allowed yet
		self.c = {i: self[i] for i in range(self.min, self.max+1)} # Fill in missing entries
		self.c_plus = self.cdf(a=1)
		
	def __add__(self, other):
		m = min(self.min, other.min)
		M = max(self.max, other.max)

		assert self.min == 0  # np.convolve might require this assumption
		assert other.min == 0  # But this should be checked if allowing negatives.

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

	@staticmethod
	def join(original, other, probability_of_other):
		""" Returns the distribution that combines self and other with a relative probability.
	
		So if there is an x chance of drawing damage from distribution A, 
		and a (1-x) probability of drawing damage from distribution B, 
		then A.join(B, x) gives the new damage distribution.
		"""
		p_b = probability_of_other
		p_a = 1 - p_b
		M = max( max(list(original.keys())), max(list(other.keys())) )
		c = {}
		for d in range(0, M + 1):
			c[d] = p_a*original.get(d, 0) + p_b*other.get(d, 0)
		return c

	@staticmethod
	def scale(original, scaling):
		""" Returns the distribution where damage is scaled by the scaling factor.
		"""
		c = {}
		for d, p in original.items():
			d = floor(d * scaling)
			c[d] = c.get(d, 0) + p
		return c

	@property
	def mean(self):
		return np.average(list(self.c.keys()), weights=list(self.c.values()))

	@property
	def max(self):
		return list(self.c.keys())[-1]

	@property
	def min(self):
		return list(self.c.keys())[0]

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
	triple = DamageDistribution.scale(normal, 3)
	return DamageDistribution.join(normal, triple, 1/51)

def verac(m, a):
	normal = standard(m, a)
	perfect = {d+1: p for d, p in standard(m, 1).items()}
	return DamageDistribution.join(normal, perfect, 1/4)

def gadderhammer(m, a):
	normal = standard(m, a)
	double = DamageDistribution.scale(normal,2)
	return DamageDistribution.join(normal, double, 5/100)

def ahrim(m, a):
	normal = standard(m, a)
	boosted = DamageDistribution.scale(normal,1.3)
	return DamageDistribution.join(normal, boosted, 25/100)

def karil(m, a):
	normal = standard(m, a)
	boosted = DamageDistribution.scale(normal,1.5)
	return DamageDistribution.join(normal, boosted, 25/100)

def scythe(m, a):
	normal = standard(m, a)
	half = DamageDistribution.scale(normal, 0.5)
	quarter = DamageDistribution.scale(normal,0.25)
	return (  # Acts like 3 separate fighters
		DamageDistribution(normal) +
		DamageDistribution(half) +
		DamageDistribution(quarter)
	).c

def opal(m, a, visible_ranged_level, diary=True):
	increase = floor(0.1*visible_ranged_level)
	normal = standard(m, a)
	bolt = standard(m + increase, a)
	return DamageDistribution.join(normal, bolt, (5.5/100) if diary else (5/100))

def pearl(m, a, visible_ranged_level, fiery, diary=True):
	if fiery:
		increase = floor(visible_ranged_level/15)
	else:
		increase = floor(visible_ranged_level/20)
	normal = standard(m, a)
	bolt = standard(m + increase, a)
	return DamageDistribution.join(normal, bolt, (6.6/100) if diary else (6/100))

def diamond(m, a, diary=True):
	increase = floor(0.15*m)
	normal = standard(m, a)
	bolt = standard(m + increase, 1)
	return DamageDistribution.join(normal, bolt, (11/100) if diary else (10/100))

def dragon(m, a, visible_ranged_level, diary=True):
	increase = floor(0.2*visible_ranged_level)
	normal = standard(m, a)
	bolt = standard(m + increase, a)
	return DamageDistribution.join(normal, bolt, (6.6/100) if diary else (6/100))

def onyx(m, a, diary=True):
	increase = floor(0.2*m)
	normal = standard(m, a)
	bolt = standard(m + increase, a)
	return DamageDistribution.join(normal, bolt, (11/100) if diary else (10/100))

def brimstone_ring(m, attack_roll, defence_roll):
	# assumes magic attack
	normal_accuracy = accuracy.accuracy(attack_roll, defence_roll)
	special_accuracy = accuracy.accuracy(attack_roll, int(0.9*defence_roll))
	normal = standard(m, normal_accuracy)
	special = standard(m, special_accuracy)
	return DamageDistribution.join(normal, special, 25/100)

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
	combined = DamageDistribution.join(melee, ranged, 1/3)
	
	general = DamageDistribution(combined)
	stack = DamageDistribution(standard(15, 0.25))
	will = DamageDistribution(standard(16, 0.30))
	spike = DamageDistribution(standard(21, 0.16))

	return (general + stack + will + spike).c
	

	

if __name__ == '__main__':

	from osrsmath.skills.combat.temp.probabilities import Solution2
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
	