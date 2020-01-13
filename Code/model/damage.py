""" This file provides an methods for calculating damage according to equipment bonuses,
	combat levels and boosts for the various combat styles.

	@todo: Add ranged and magic

	Note: Several calculations assume that the 'other' multipler occurs to the base
	        damage (instead of in the effective level calculation) this seems weird to
	        me since it modifies the effective_level calculation.
	        @see max_attack_roll_alternate vs max_attack_roll
"""


from math import floor

def effective_level(level, B_pot, B_pray, B_other, B_style, constant):
	return floor((level + B_pot) * B_pray * B_other) + B_style + constant

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
		return floor(self.base_damage(E_str, str_level, B_pot, B_pray, B_other, B_style) * B_SA * multipler)

	def accuracy(self, max_attacker_roll, max_defender_roll):
		A_max = max_attacker_roll
		D_max = max_defender_roll
		if A_max >= D_max:
			return 1 - 0.5 * (D_max + 2) / (A_max + 1)
		else:
			return A_max / (2 * D_max + 2)
