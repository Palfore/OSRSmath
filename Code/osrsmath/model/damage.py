""" This file provides an methods for calculating damage according to equipment bonuses,
	combat levels and boosts for the various combat styles.

	@todo: Add ranged and magic
"""

from math import floor

def effective_level(level, B_pot, B_pray, B_other, B_style, constant):
	return floor((level + B_pot) * B_pray * B_other) + B_style + constant


def average(h, M):
	""" Returns the expected damage on a given hit. """
	if h >= M:
		return M / 2
	else:
		return (h/2) * (2 - (h + 1) / (M + 1))

class Melee:
	def base_damage(self, E_str, str_level, B_pot, B_pray, B_other, B_style):
		C = [1.3, 1/10., 1/80., 1/640.]
		S_eff = effective_level(str_level, B_pot, B_pray, B_other, B_style, 0)
		return C[0] + C[1]*S_eff + C[2]*E_str + C[3]*E_str*S_eff

	def max_attack_roll(self, E_att, att_level, B_pot, B_pray, B_other, B_style, multipler):
		A_eff = effective_level(att_level, B_pot, B_pray, B_other, B_style, 8)
		return floor(A_eff*(E_att + 64)*multipler)

	def max_defence_roll(self, E_def, def_level, B_pot, B_pray, B_other, B_style, multipler):
		D_eff = effective_level(def_level, B_pot, B_pray, B_other, B_style, 8)
		return floor(D_eff*(E_def + 64)*multipler)

	def max_hit(self, E_str, str_level, B_pot, B_pray, B_other, B_style, B_SA, multipler):
		M = floor(self.base_damage(E_str, str_level, B_pot, B_pray, B_other, B_style) * B_SA * multipler)
		assert M >= 1, [E_str, str_level, B_pot, B_pray, B_other, B_style, B_SA, multipler]
		return M

	@staticmethod
	def accuracy(max_attacker_roll, max_defender_roll):
		A_max = max_attacker_roll
		D_max = max_defender_roll
		assert A_max >= 0
		assert D_max >= 0
		if A_max >= D_max:
			return 1 - 0.5 * (D_max + 2) / (A_max + 1)
		else:
			return A_max / (2 * D_max + 2)


if __name__ == '__main__':
	from matplotlib import pyplot as PLT
	from matplotlib import cm as CM
	from matplotlib import mlab as ML
	import numpy as np

	x = np.array(range(0, 1000+1))
	y = np.array(range(0, 1000+1))
	X, Y = np.meshgrid(x, y)

	Z = np.array([np.array([ Melee.accuracy(a, d) for d in x]) for a in y])

	x = X.ravel()
	y = Y.ravel()
	z = Z.ravel()

	PLT.hexbin(x, y, C=z, cmap='RdBu', bins=None)
	PLT.axis([x.min(), x.max(), y.min(), y.max()])

	cb = PLT.colorbar()
	cb.set_label('mean value')
	PLT.show()