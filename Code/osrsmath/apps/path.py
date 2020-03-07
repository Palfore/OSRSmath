from osrsmath.model.monsters import Monster, get_monster_data
from osrsmath.model.player import Player, get_equipment_data
from osrsmath.model.rates import experience_per_hour
import osrsmath.model.boosts as boosts
from osrsmath.model import successful_hits
from pprint import pprint
import numpy as np
import copy

def get_player(equipment_data=None, attack=70, strength=86, combat_style='slash'):
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
	attacker.combat_style = combat_style
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

def average_xp(attacker, model, m, A, attack_speed, defender_ids):
	average = 0
	attackers_attack_type = attacker.get_stances()[attacker.combat_style]['attack_type']
	max_name_length = max(len(name) for name in defender_ids)
	for name, defender in defender_ids.items():
		D = defender.get_defence_roll(attackers_attack_type, 0, 1, 1, 1)
		a = Player.get_accuracy(A, D)
		E = experience_per_hour(defender.levels['hitpoints'], m, a, 1 / attack_speed, 4, getattr(successful_hits, model)())
		average += E
	average /= len(defender_ids)
	return average

def time_dependent_model_xp(attacker, model, defender_ids, min_att_boost):
	# Assumes super combat potion used, and potion re-drank after less than min_att_boost boosts.
	# ie I drink a super combat potion every time my attack falls below attack_level+min_att_boost.
	attacker = copy.deepcopy(attacker)
	a = attacker.levels['attack']
	s = attacker.levels['strength']

	#############
	m = attacker.get_max_hit(0, 1, 1, 1)
	A = attacker.get_attack_roll(0, 1, 1, 1)
	if min_att_boost is None:
		return average_xp(attacker, model, m, A, attacker.get_stats()['attack_speed'], defender_ids)



	ds = boosts.super_potion(s)
	da = boosts.super_potion(a)

	xp = 0
	for t in range(da-min_att_boost+1):
		attacker.levels['attack'] = a + da - t
		attacker.levels['strength'] = s + ds - t
		m = attacker.get_max_hit(0, 1, 1, 1)
		A = attacker.get_attack_roll(0, 1, 1, 1)

		average = average_xp(attacker, model, m, A, attacker.get_stats()['attack_speed'], defender_ids)
		xp += average
	xp /= da - min_att_boost + 1
	return xp


###########################################
def get_xp(attack, strength, training, defenders, equipment_data, min_att_boost):
	attacker = get_player(equipment_data, attack=attack, strength=strength, combat_style={
		'attack': 'chop', 'strength': 'slash',
	}[training])
	return time_dependent_model_xp(attacker, 'Recursive', defenders, min_att_boost=min_att_boost)


from math import floor
def experience_till_next_level(level):
	x = level - 1
	return floor( x + 300 * 2**(x / 7) ) / 4

def format(parent, child, min_att_boost, defenders, equipment_data):
	def f(pair):
		return f"{pair[0]}-{pair[1]}"
	(old_a, old_s), (new_a, new_s) = parent, child
	training_style = 'attack' if new_a > old_a else 'strength'
	training_level = old_a if new_a > old_a else old_s
	return f(parent), f(child), get_time(parent, training_style, training_level, min_att_boost, defenders, equipment_data)

def get_time(node, training_style, training_level, min_att_boost, defenders, equipment_data):
	xp_per_hour = get_xp(*node, training_style, min_att_boost, defenders, equipment_data)
	return experience_till_next_level(training_level) / xp_per_hour

def g(parents):
	children = []
	seen = []
	for _, (x, y) in parents:
		if (x, y) in seen:
			continue
		seen.append((x, y))
		if x != 99:
			children.append(((x, y), (x+1, y)))
		if y != 99:
			children.append(((x, y), (x, y+1)))
	return children

def h(x, y):
	nodes = []
	def recur(parents):
		if parents:
			children = g(parents)
			nodes.extend(children)
			print(len(nodes), len(children))
			recur(children)
	recur([ ((None, None), (x, y)) ])
	return nodes



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

def get_solution(a, s, min_att_boost, defenders, equipment_data):
	graph = Graph()
	nodes = h(a, s)
	print(nodes[0])
	print(len(nodes))

	nodes = xmap(lambda c: format(*c, defenders, equipment_data, min_att_boost), nodes)

	[graph.add_edge(*node) for node in nodes]
	path = find_path(graph, f'{a}-{s}', '99-99')
	return path

if __name__ == '__main__':
	from pprint import pprint
	from dijkstar import Graph, find_path

	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt
	import numpy as np

	equipment_data_ = get_equipment_data()
	monster_data_ = get_monster_data()
	difficulty_ = 'easy-potions'
	defenders_ = get_opponents(monster_data_)[difficulty_.split('-')[0]]
	x, y = 60, 60
	path = get_solution(x, y, None, defenders_, equipment_data_)


	# print(path)
	# s = 0
	# for i in range(60, 99):
	# 	parent = (i, 60)
	# 	child = (i+1, 60)
	# 	p, c, t = format(parent, child, defenders_, equipment_data_, 5)
	# 	print(p, c, t)
	# 	s += t

	# for i in range(60, 99):
	# 	parent = (99, i)
	# 	child = (99, i+1)
	# 	p, c, t = format(parent, child, defenders_, equipment_data_, 5)
	# 	print(p, c, t)
	# 	s += t

	# print(s)
	# exit()

	leveled_skill = []
	prev_a, prev_s = 0, 0
	for n, cost in zip(path.nodes, path.costs):
		a, s = n.split('-')
		a, s = int(a), int(s)
		print(n.replace('-', ', '), cost)
		if a > prev_a:
			leveled_skill.append(0)
		elif s > prev_s:
			leveled_skill.append(1)
		prev_a, prev_s = a, s
	print(path.total_cost)


	time_for_next_level_data = []
	path = get_solution(x, y, 5, defenders_, equipment_data_)
	leveled_skill2 = []
	prev_a, prev_s = 0, 0
	for n, cost in zip(path.nodes, path.costs):
		a, s = n.split('-')
		a, s = int(a), int(s)
		print(n.replace('-', ', '), cost)
		time_for_next_level_data.append(cost)
		if a > prev_a:
			leveled_skill2.append(0)
		elif s > prev_s:
			leveled_skill2.append(1)
		prev_a, prev_s = a, s
	print(path.total_cost)


	# from Helpers.graph import Graph
	# Graph("Results/time_to_level/time.agr", "test", [
	# 	(None, [
	# 		(None, 'xy', zip(list(range(len(time_for_next_level_data))), time_for_next_level_data))
	# 	])
	# ])

	# exit()

	fig, (ax0, ax1) = plt.subplots(2, 1)
	ax0.set_yticklabels([])
	print(plt.xticks())

	plt.xlabel("Levels Obtained")
	ax0.set_xticks([0.0, len(leveled_skill)])
	ax0.set_xticklabels([f"{x}, {y}", f"{99}, {99}"])
	ax0.tick_params(axis='y', which='both', left=False, right=False, labelbottom=False)
	ax0.set_title("No Potions", loc='center')
	ax0.pcolor(np.array([leveled_skill, ]), cmap=plt.cm.get_cmap('prism_r', 2), edgecolors='black')  # Wistia

	# labels = [item.get_text() for item in ax0.get_xticklabels()]
	# labels[0] = f"{x}, {y}"
	# labels[-2] = f"{99}, {99}"
	# ax0.set_xticklabels(labels)

	ax1.set_yticklabels([])
	ax1.tick_params(axis='y', which='both', left=False, right=False, labelbottom=False)
	ax1.set_title("Potions", loc='center')
	ax1.pcolor(np.array([leveled_skill2, ]), cmap=plt.cm.get_cmap('prism_r', 2), edgecolors='black')  # Wistia

	import osrsmath.config as config
	import os
	plt.savefig(f"recur_{x}_{y}.pdf")
	plt.savefig(f"recur_{x}_{y}.png")
	plt.show()

