""" Notes:
	Logic is primarily translated from https://docs.google.com/spreadsheets/d/14ddt-IrH3dmcB7REE1y5AZD51I6dGBfFehQrHp1j1iQ/edit#gid=196557
"""
from math import floor
from osrsmath.combat.items import ITEM_DATABASE
from osrsmath.combat.spells import SPELLBOOK
from pprint import pprint 

class CannotAttackException(ValueError):
	pass


def defence_roll(stance, gear, opponent, visible_levels, prayers, spell=None):
	# Assumes everything is valid, i.e. player.can_attack() == True
	assert not prayers  # Not yet handled
	if stance['combat_class'] == 'melee':
		if spell is not None:
			raise ValueError(f'The spell is set to "{spell}", but should be None.')
		return melee_defence_roll(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			visible_levels['defence'],
			sum(i['equipment'][f"defence_{opponent.stance['attack_type']}"] for i in gear.values()),
			prayer_multiplier=1.0
		)
	else:
		raise CannotAttackException(f"No combat class could be determined for {stance['combat_style']}.")

def melee_defence_roll(stance, equipment, opponent, visible_defence_level, equipment_defence, prayer_multiplier):
	""" Calculates the max defence roll for a given setup.

	Args:
		stance: dict, the stance of the attacker.
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.
	"""
	if stance['attack_type'] not in ['slash', 'stab', 'crush']:
		raise CannotAttackException(f'Invalid attack type in given stance: {stance}. Must be one of [slash, stab, crush].')
	if stance['attack_style'] not in ['accurate', 'aggressive', 'controlled', 'defensive']:
		raise CannotAttackException(f'Invalid attack style in given stance: {stance}. Must be one of [accurate, aggressive, controlled, defensive].')

	stance_bonus = 0
	stance_bonus = {'defensive': 11, 'long': 11, 'controlled': 9}.get(stance['attack_style'], 8)
	defence_level = int(visible_defence_level * prayer_multiplier + stance_bonus)
	D =  int( (9 + defence_level) * (64 + equipment_defence) )
	return D



if __name__ == '__main__':
	from osrsmath.combat.items import ITEM_DATABASE
	from pprint import pprint
	from osrsmath.combat.fighter import Fighter
	from osrsmath.combat.accuracy import *
	from osrsmath.combat.damage import damage
	import osrsmath.combat.distributions as distributions

	dscim = ITEM_DATABASE.find('Dragon scimitar')
	runek = ITEM_DATABASE.find('Rune kiteshield')
	
	A = Fighter(99, {
			'attack': 90,
			'strength': 90,
			'defence': 90,
		}, [
			'Dragon scimitar',
		]
	)
	A.set_stance('chop')
	D = Fighter(200, {
			'attack': 90,
			'strength': 75,
			'defence': 54,
		}, [
			'Rune longsword',
			'Rune kiteshield',
		]
	)
	D.set_stance('block')

	print('Attacker')
	print(A.max_hit(D))
	print(A.attack_roll(D))
	print(A.defence_roll(D))
	print(A.accuracy(D))
	print()
	print('Defender')
	print(D.max_hit(A))
	print(D.attack_roll(A))
	print(D.defence_roll(A))
	print(D.accuracy(A))
	print()

	A_DD = distributions.DamageDistribution(A.damage_distribution(D))
	D_DD = distributions.DamageDistribution(D.damage_distribution(A))
	
	from math import sqrt
	print('Kill times')
	A_atk = A.expected_turns_to_kill(D)
	A_var = sqrt(A.variance(D))
	D_atk = D.expected_turns_to_kill(A)
	D_var = sqrt(D.variance(A))
	print(A_var, D_var)
	import matplotlib.pyplot as plt

	L_max = 120
	plt.plot([A_DD.P(D.hitpoints, L) for L in range(1, L_max)], color='black')
	plt.plot([D_DD.P(A.hitpoints, L) for L in range(1, L_max)], color='red')
	plt.hlines(A_DD.P(D.hitpoints, floor(A_atk)) / 2, A_atk - A_var, A_atk + A_var, color='black')
	plt.hlines(D_DD.P(A.hitpoints, floor(D_atk)) / 2, D_atk - D_var, D_atk + D_var, color='red')
	plt.axvline(A_atk, color='black')
	plt.axvline(D_atk, color='red')
	plt.show()
	# .plot().show()




	