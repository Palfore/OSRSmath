""" Notes:
	Logic is primarily translated from https://docs.google.com/spreadsheets/d/14ddt-IrH3dmcB7REE1y5AZD51I6dGBfFehQrHp1j1iQ/edit#gid=196557
"""
from math import floor
from osrsmath.skills.combat.items import ITEM_DATABASE
from osrsmath.skills.combat.spells import SPELLBOOK
from pprint import pprint 

class CannotAttackException(ValueError):
	pass


def defence_roll(stance, gear, opponent, visible_levels, prayers, spell=None):
	# Assumes everything is valid, i.e. player.can_attack() == True
	assert not prayers  # Not yet handled
	if opponent.spell is not None or opponent.stance['combat_class'] == 'magic':
		return magic_defence_roll(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			visible_levels['defence'],
			visible_levels['magic'],
			sum(i['equipment'][f"defence_magic"] for i in gear.values()),
			prayer_multiplier=1.0
		)
	elif opponent.stance['combat_class'] == 'ranged':
		return ranged_defence_roll(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			visible_levels['defence'],
			sum(i['equipment'][f"defence_ranged"] for i in gear.values()),
			prayer_multiplier=1.0
		)
	elif opponent.stance['combat_class'] == 'melee':
		return melee_defence_roll(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			visible_levels['defence'],
			sum(i['equipment'][f"defence_{opponent.stance['attack_type']}"] for i in gear.values()),
			prayer_multiplier=1.0
		)
	else:
		raise ValueError(f"No combat class could be determined for {stance['combat_style']}.")


def melee_defence_roll(stance, equipment, opponent, visible_defence_level, equipment_defence, prayer_multiplier):
	""" Calculates the max defence roll for a given setup.

	Args:
		stance: dict, the stance of the attacker.
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.
	"""
	# valid_attack_types = ['slash', 'stab', 'crush']
	# valid_attack_styles = ['accurate', 'aggressive', 'controlled', 'defensive']
	# if stance['attack_type'] not in valid_attack_types:
	# 	raise CannotAttackException(f'Invalid attack type in given stance: {stance}. Must be one of {valid_attack_types}.')
	# if stance['attack_style'] not in valid_attack_styles:
	# 	raise CannotAttackException(f'Invalid attack style in given stance: {stance}. Must be one of {valid_attack_styles}.')

	stance_bonus = {'defensive': 11, 'long': 11, 'controlled': 9}.get(stance['attack_style'], 8)
	defence_level = int(visible_defence_level * prayer_multiplier + stance_bonus)
	D = int( (9 + defence_level) * (64 + equipment_defence) )
	return D


def ranged_defence_roll(stance, equipment, opponent, visible_defence_level, equipment_defence, prayer_multiplier):
	""" Calculates the max defence roll for a given setup.

	Args:
		stance: dict, the stance of the attacker.
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.
	"""
	# valid_attack_types = [None]
	# valid_attack_styles = [None]
	# if stance['attack_type'] not in valid_attack_types:
	# 	raise CannotAttackException(f'Invalid attack type in given stance: {stance}. Must be one of {valid_attack_types}.')
	# if stance['attack_style'] not in valid_attack_styles:
	# 	raise CannotAttackException(f'Invalid attack style in given stance: {stance}. Must be one of {valid_attack_styles}.')

	stance_bonus = {'defensive': 11, 'long': 11, 'controlled': 9}.get(stance['attack_style'], 8)
	defence_level = int(visible_defence_level * prayer_multiplier + stance_bonus)
	D = int( (9 + defence_level) * (64 + equipment_defence) )
	return D


def magic_defence_roll(stance, equipment, opponent, visible_defence_level, visible_magic_level, equipment_defence, prayer_multiplier):
	""" Calculates the max defence roll for a given setup.

	Args:
		stance: dict, the stance of the attacker.
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.
	"""
	# if spell is None:
	# 	if stance['weapon_type'] != 'trident-class_weapons':
	# 		raise ValueError("Without a spell, only trident-class_weapons can attack with magic.")
	
	stance_bonus = {'defensive': 11, 'long': 11, 'controlled': 9}.get(stance['attack_style'], 8)
	defence_level = int(visible_defence_level * prayer_multiplier + stance_bonus)
	D =  int(0.3*defence_level) + int(0.7*visible_magic_level)
	return D * (64 + equipment_defence)


if __name__ == '__main__':
	from osrsmath.skills.combat.items import ITEM_DATABASE
	from pprint import pprint
	from osrsmath.skills.combat.fighter import Fighter, Duel
	from osrsmath.skills.combat.accuracy import *
	from osrsmath.skills.combat.damage import damage
	import osrsmath.skills.combat.distributions as distributions

	dscim = ITEM_DATABASE.find('Dragon scimitar')
	runek = ITEM_DATABASE.find('Rune kiteshield')
	

	def fighters(strength):
		D = Fighter(90, {
				'attack': 75,
				'strength': 75,
				'defence': 75,
				'magic': 75,
			}, [
				# 'Staff of air',
				'Rune kiteshield',
				'Rune sword',
			],
			attributes=['kalphite']
		)
		
		# D.set_stance('chop')
		# D.set_spell('Wind wave')

		# A = Fighter(90, {
		# 		'attack': 80,
		# 		'strength': strength,
		# 		'defence': 80,
		# 		'magic': 80
		# 	}, [
		# 		'Keris',
		# 		'Rune kiteshield',
		# 	]
		# )
		# A.set_stance('block')

		A = Fighter(90, {
				'attack': strength,
				'strength': strength,
				'ranged': strength,
				'defence': strength,
				'magic': strength
			}, [
				'Rune kiteshield',
				'Rune sword',
				# 'Keris',
				# 'Iron dart',
				# 'Bandos godsword'
				# "Dharok's greataxe"

			]
		)
		# A.set_stance('block')
		# pprint(A.gear['weapon'])
		# A.set_stance('chop')
		# A.set_stance('accurate')
		# A.set_stance('rapid')
		# pprint(A.stance)
		# print(A.attack_speed())
		# print(A.attack_interval())
		# exit()
		return A, D
	
	# Future note: To optimize:
	# 	[set of loadouts] --stats, etc. | minimize: expected_turns_to_kill--> optimal loadout
	A, D = fighters(90)
	print('Attacker')
	print(f"m={A.max_hit(D)}, a={A.accuracy(D)}, w={A.attack_speed()}")
	print(A.attack_roll(D))
	print(A.defence_roll(D))
	print()
	print('Defender')
	print(f"m={D.max_hit(A)}, a={D.accuracy(A)}, w={D.attack_speed()}")
	print(D.attack_roll(A))
	print(D.defence_roll(A))
	print()
	print('Results')


	# print(A.P_kill(D).min())
	
	# for L in range(1, 100):
		# print(L, A.P_kill(D).pmf(L))
		# print(L, A.P_kill(D).pmf(L))
	# print(A.P_kill(D).pmf(14))
	# print()
	from math import sqrt
	import matplotlib.pyplot as plt
	# Plotting Damage Distributions
	# plt.bar(A.damage_distribution(D).c.keys(), A.damage_distribution(D).c.values())
	# plt.bar(D.damage_distribution(A).c.keys(), D.damage_distribution(A).c.values())
	# plt.show()
	# exit()

	duel = Duel(A, D, delays=(0, 2))
	# print(duel.turns_to_kill())
	print('Mean')
	# duel.P_attacker()
	print(duel.P_attacker.pmf(20))
	# print(duel.P_attacker.cutoff())
	# print(duel.P_defender.cutoff())
	# print('??', duel.P_defender.quantile(p=1))
	# print('>>',duel.P_defender.quantile(p=0.95))
	# exit()
	print('Start==========================')
	print(duel.P_win())
	print(duel.P_lose())
	print(duel.P_draw())
	print(duel.P_top(0.10))
	print(duel.P_win() + duel.P_lose() + duel.P_draw())
	# exit()
	print()
	x = range(10, 100+1)
	ys = []
	import time
	start = time.time()
	# for strength in x:
	# 	duel = Duel(*fighters(strength))
	# 	outcomes = duel.outcomes()
	# 	ys.append(outcomes)
	# 	print(strength, duel.P_win(), sum(outcomes))
	# print(time.time() - start)
	# ys = list(map(list, zip(*ys)))

	for strength in x:
		duel = Duel(*fighters(strength), tol=1e-1)
		outcomes = duel.outcomes()
		L = duel.expected_turns_to_kill()
		L2 = duel.expected_turns_to_die()
		# ys.append(outcomes)
		ys.append([L, L2])
		print(strength, duel.P_win(), sum(outcomes), L)
	print(time.time() - start)
	ys = list(map(list, zip(*ys)))

	for y in ys:
		plt.plot(x, y)
	plt.show()


	# print(duel.P_attacker.mean())
	# print(duel.P_win())
	exit()


	# A_DD = A.damage_distribution(D)
	# D_DD = D.damage_distribution(A)
	
	# A_DD.plot()
	# D_DD.plot()
	# plt.show()

	# print('Kill times')
	# A_atk = A.expected_turns_to_kill(D)
	# A_var = sqrt(A.variance(D))
	# D_atk = D.expected_turns_to_kill(A)
	# D_var = sqrt(D.variance(A))
	# print(A_var, D_var)

	# L_max = 120
	# plt.plot([A_DD.P(D.hitpoints, L) for L in range(1, L_max)], color='black')
	# plt.plot([D_DD.P(A.hitpoints, L) for L in range(1, L_max)], color='red')
	# plt.hlines(A_DD.P(D.hitpoints, floor(A_atk)) / 2, A_atk - A_var, A_atk + A_var, color='black')
	# plt.hlines(D_DD.P(A.hitpoints, floor(D_atk)) / 2, D_atk - D_var, D_atk + D_var, color='red')
	# plt.axvline(A_atk, color='black')
	# plt.axvline(D_atk, color='red')
	# plt.show()
	# .plot().show()




	