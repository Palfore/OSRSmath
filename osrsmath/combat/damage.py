""" This file provides an methods for calculating damage according to equipment bonuses,
	combat levels and boosts for the various combat styles. It is possible that the flooring
	is not accurate. These are very difficult to discover, and I'm not sure if any one has
	an official source on the flooring order. If anyone does, please contact me or update this.

	In addition, negative attack bonuses are not handled since their implementation is unknown.
"""

from osrsmath.combat.spells import get_spell
from math import floor

def effective_level(level, B_pot, B_pray, B_other, B_style, constant):
	return floor((level + B_pot) * B_pray * B_other) + B_style + constant

def average(h, M):
	""" Returns the expected damage on a given hit. """
	if h >= M:
		return M / 2
	else:
		return (h/2) * (2 - (h + 1) / (M + 1))

def accuracy(max_attacker_roll, max_defender_roll):
	A_max = max_attacker_roll
	D_max = max_defender_roll
	assert A_max >= 0  # Not sure how to handle negative attack bonuses, clamp?
	assert D_max >= 0
	if A_max >= D_max:
		return 1 - 0.5 * (D_max + 2) / (A_max + 1)
	else:
		return A_max / (2 * D_max + 2)

class Standard:
	def max_hit(self, E_str, str_level, B_pot, B_pray, B_other, B_style, B_SA, multiplier):
		""" B_other gets applied inside floor, multiplier gets applied outside. """
		C = [1.3, 1/10., 1/80., 1/640.]
		S_eff = effective_level(str_level, B_pot, B_pray, B_other, B_style, 0)
		base_damage = C[0] + C[1]*S_eff + C[2]*E_str + C[3]*E_str*S_eff
		M = floor(base_damage * B_SA) * multiplier
		assert M >= 1, [E_str, str_level, B_pot, B_pray, B_other, B_style, B_SA, multiplier]
		return floor(M)

	def max_attack_roll(self, E_att, att_level, B_pot, B_pray, B_other, B_style, multiplier):
		A_eff = effective_level(att_level, B_pot, B_pray, B_other, B_style, 8)
		return floor(A_eff*(E_att + 64)*multiplier)

	def max_defence_roll(self, E_def, def_level, B_pot, B_pray, B_other, B_style, multiplier):
		D_eff = effective_level(def_level, B_pot, B_pray, B_other, B_style, 8)
		return floor(D_eff*(E_def + 64)*multiplier)


class Magic:
	def max_hit(self, spell, E_str, str_level, B_pot, B_pray, B_other, B_SA, multipler):
		""" 
			str_level on matters for magic dart, salamanders, and trident of the seas/swamp. 
			Potions only boost damage for those spells
			There are no prayers that increase magic damage
			Also tome of fire, chaos gauntlets
		"""
		base_damage = get_spell(spell)['max_hit']
		return floor(base_damage * (1 + E_str/100))

	def max_attack_roll(self, E_att, att_level, B_pot, B_pray, B_other, B_style, multiplier):
		M_eff = effective_level(att_level, B_pot, B_pray, B_other, 0, 8)
		return floor(M_eff * (E_att + 64))

	def max_defence_roll(self, E_def, magic_level):
		""" Only PvM is supported now """
		return magic_level * (64 + E_def)

