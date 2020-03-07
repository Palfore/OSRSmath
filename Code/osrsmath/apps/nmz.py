from model.monsters import Monster, get_monster_data
from model.player import Player, get_equipment_data
from model.rates import experience_per_hour
from model import successful_hits
from pprint import pprint
import numpy as np
import copy

def get_player(equipment_data=None, attack=70, strength=86):
	if equipment_data is None:
		equipment_data = get_equipment_data()
	attacker = Player({'attack': attack, 'strength': strength, 'defence': 70, 'prayer': 56, 'hitpoints': 79, 'magic': 71, 'ranged': 70})
	attacker.equip_by_name("Dragon Scimitar", equipment_data)
	attacker.equip_by_name("Dharok's helm", equipment_data)
	attacker.equip_by_name("Dharok's platebody", equipment_data)
	attacker.equip_by_name("Dharok's platelegs", equipment_data)
	attacker.equip_by_name("Dragon Boots", equipment_data)
	attacker.equip_by_name("Holy Blessing", equipment_data)
	attacker.equip_by_name("Barrows Gloves", equipment_data)
	attacker.equip_by_name("Dragon Defender", equipment_data)
	attacker.equip_by_name("Berserker Ring (i)", equipment_data)
	attacker.equip_by_name("Amulet of Fury", equipment_data)
	attacker.equip_by_name("Fire Cape", equipment_data)
	attacker.combat_style = 'slash'
	return attacker

def get_opponents(monster_data=None):
	if monster_data is None:
		monster_data = get_monster_data()
	king_roald_hard = Monster({'attack': 140, 'strength': 120, 'defence': 30, 'prayer': 1, 'hitpoints': 150, 'magic': 1, 'ranged': 1})
	king_roald_hard.attack_style = 'crush'
	defenders = {
		'easy': {
			'Count Draynor': Monster.from_id(6393),
			'King Roald': Monster.from_id(6389),
			'Me': Monster.from_id(6381),
			'Tree Spirit': Monster.from_id(6380),
			'Khazard Warlord': 	Monster.from_id(6390),
		}, 'hard': {
			'Count Draynor': Monster.from_id(6332),
			'King Roald': king_roald_hard,
			'Me': Monster.from_id(6320),
			'Tree Spirit': Monster.from_id(6319),
			'Khazard Warlord': Monster.from_id(6329),
		}
	}
	return defenders

def average_xp(model, m, A, attack_speed, defender_ids):
	average = 0
	attackers_attack_type = attacker.get_stances()[attacker.combat_style]['attack_type']
	max_name_length = max(len(name) for name in defenders)
	for name, defender in defenders.items():
		D = defender.get_defence_roll(attackers_attack_type, 0, 1, 1, 1)
		a = Player.get_accuracy(A, D)
		E = experience_per_hour(defender.levels['hitpoints'], m, a, 1 / attack_speed, 4, getattr(successful_hits, model)())
		average += E
		# print(f"({name:{max_name_length}s}), HP: {defender.levels['hitpoints']}, Defence Roll: {D}, Accuracy: {a:.5f}, XP/H: {E:.2f}")
	average /= len(defender_ids)
	return average

def average_model_xp(model, m, A, defender_ids, true_value):
	print(f"Model: {model}, Max hit: {m}, Attack roll: {A}")
	average = average_xp(model, m, A, defender_ids)
	percent_error = abs(1-average/true_value)*100
	print(f"Average XP/h: {average:.2f} => {average/1000:.1f}k    {percent_error:1.1f}%")
	return average, percent_error

def time_dependent_model_xp(attacker, model, defender_ids, min_att_boost):
	# Assumes super combat potion used, and potion re-drank after less than min_att_boost boosts.
	# ie I drink a super combat potion every time my attack falls below attack_level+min_att_boost.
	attacker = copy.deepcopy(attacker)
	a = attacker.levels['attack']
	s = attacker.levels['strength']
	ds = boosts.super_potion(s)
	da = boosts.super_potion(a)

	xp = 0
	for t in range(da-min_att_boost+1):
		attacker.levels['attack'] = a + da - t
		attacker.levels['strength'] = s + ds - t
		m = attacker.get_max_hit(0, 1, 1, 1)
		A = attacker.get_attack_roll(0, 1, 1, 1)

		average = average_xp(model, m, A, attacker.get_stats()['attack_speed'], defenders)
		xp += average
		# print(t, a, s, da, ds, m, A, average)
	xp /= da - min_att_boost + 1
	return xp


if __name__ == '__main__':
	import model.boosts as boosts

	# Retrieve Data
	equipment_data = get_equipment_data()
	monster_data = get_monster_data()
	attacker = get_player(equipment_data, strength=90)  # 89, 90, 91
	print(f"M in [{attacker.get_max_hit(0, 1, 1, 1)}..{attacker.get_max_hit(boosts.super_potion(attacker.levels['strength']), 1, 1, 1)}]")


	# Determine Experience Rates
	difficulty = 'hard-potions'
	defenders = get_opponents(monster_data)[difficulty.split('-')[0]]
	experimental_data = {  # as (xp/h, experimental_time) pairs
		'easy':         [(57.1*1000,       1.47), (58.3*1000,        2.9),     (58*1000, 124.4/58), (58.6*1000, 108.4/58.6)],
		'hard':         [(64.5*1000, 132.5/64.5), (64.3*1000,  85.7/64.3),    (63.7*1000, 81/63.7), (64.7*1000, 108.0/64.7), (65.0*1000, 121.3/65.0)],
		'easy-potions': [(67.9*1000, 106.5/67.9), (66.0*1000, 132.1/67.9), (67.8*1000, 122.1/67.9), (68.7*1000, 104.0/67.9)], # 89 str
		'hard-potions': [(74.8*1000, 134.6/74.8), (74.7*1000, 119.3/74.7), (76.3*1000, 137.2/76.3), (73.7*1000, 119.0/73.7)], # 90 str
	}

	experimental_rates = {}
	for diff, data in experimental_data.items():
		rates, times = list(zip(*data))
		assert len(rates) == len(times)
		experimental_rates[diff] = np.average(rates, weights=times), np.std([
			rates[i] for i in range(len(rates))
		])
		print(f"Total experimental time ({diff}):", sum(times))
	print()


	#####################################
	xp = {}
	models = ['Crude', 'Recursive', 'Simulation', "BitterKoekje_Nukelawe"]
	for model in models:
		xp[model] = time_dependent_model_xp(attacker, model, defenders, min_att_boost=5)
		xp[model] = xp[model], abs(1-xp[model]/experimental_rates[difficulty][0])*100
		print(model, xp[model])

	pprint(xp)
	print()
	# exit()

	#############################

	# stats = attacker.get_stats()
	# m = attacker.get_max_hit(0, 1, 1, 1)
	# A = attacker.get_attack_roll(0, 1, 1, 1)
	# xp = {}
	# models = ['Crude', 'Recursive', 'Simulation', "BitterKoekje_Nukelawe"]
	# for model in models:
	# 	xp[model] = average_model_xp(model, m, A, defenders, stats['attack_speed'], experimental_rates[difficulty][0])
	# 	print()

	# pprint(xp)
	# print()
	#################################



	exp_xp_h, exp_err = experimental_rates[difficulty]
	color = lambda percent_error: 'red' if percent_error > (exp_err/exp_xp_h*100) else 'green'
	sign = lambda exp_per_hour: '+' if exp_per_hour > exp_xp_h else '-'
	latex = ' & \n'.join([
		Rf"{xp[model][0]/1000:.1f} ${sign(xp[model][0])}$\textcolor{{{color(xp[model][1])}}}{{{xp[model][1]:4.2f}\%}}"
			for model in models] +
		[Rf"{exp_xp_h/1000:.1f}$\pm${exp_err/1000:.1f} [{exp_err/exp_xp_h*100:.1f}\%]" + R'\\\\\hline\\']
	)
	print(latex)
