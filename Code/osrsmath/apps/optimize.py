from osrsmath.model.monsters import Monster, get_monster_data
from osrsmath.model.player import Player, get_equipment_data
from osrsmath.model.rates import experience_per_hour
from osrsmath.model import successful_hits
from pprint import pprint
import numpy as np

import nmz

import copy

def is_only_melee_weapon(weapon):
	return all(stance['experience'] in ('strength', 'attack', 'defence', 'shared') for stance in weapon['weapon']['stances'])

def has_offensive_melee_bonuses(armour):
	return any(amount > 0 for bonus, amount in armour['equipment'].items() if (bonus.startswith('attack') or bonus == 'melee_strength'))

if __name__ == '__main__':
	# Retrieve Data
	equipment_data = get_equipment_data()
	monster_data = get_monster_data()
	opponents = nmz.get_opponents(monster_data)

	# Reduce the equipment to only those that have a) offensive bonuses, b) melee bonuses
	# Filter for only melee weapons since other attack styles aren't handled yet
	# Also only equipment that gives offensive bonuses, since that is what we're optimizing
	for slot, equipment in equipment_data.items():
		if slot == "weapon" or slot ==  "2h":
			for ID, weapon in copy.deepcopy(equipment).items():
				if not is_only_melee_weapon(weapon):
					# print(weapon['name'])
					del equipment_data[slot][ID]
		else:
			for ID, armour in copy.deepcopy(equipment).items():
				if not has_offensive_melee_bonuses(armour):
					# print(armour['name'])
					del equipment_data[slot][ID]


	# Evolve that pool
	import random

	pop_size = 1000
	mut_chance = 0.05
	defenders = opponents['easy']

	def create_individual():
		individual = Player({'attack': 99, 'strength': 99, 'defence': 99, 'prayer': 99, 'hitpoints': 99, 'magic': 99, 'ranged': 99})
		gear = {slot: random.choice(list(equipment_data[slot].values()))['name'] for slot in equipment_data}
		for slot, equipment in gear.items():
			individual.equip_by_name(equipment, equipment_data)
		return individual


	def eval_fitness(individual):
		""" Can't handle very negative attack bonuses (-100). """
		attacker = individual['equipment']
		attacker.combat_style = list(attacker.get_stances().keys())[0]
		attackers_attack_type = attacker.get_stances()[attacker.combat_style]['attack_type']
		m = attacker.get_max_hit(0, 1, 1, 1)
		A = attacker.get_attack_roll(0, 1, 1, 1)
		average = 0.0
		for name, defender in defenders.items():
			D = defender.get_defence_roll(attackers_attack_type, 0, 1, 1, 1)
			a = Player.get_accuracy(A, D)
			E = experience_per_hour(defender.levels['hitpoints'], m, a, 1 / attacker.gear['weapon']['attack_speed'], 4, successful_hits.Crude())
			average += E
		return average

	pop = [{'equipment': create_individual(), 'fit': None} for _ in range(pop_size)]
	while True:
		for ind in pop:
			ind['fit'] = eval_fitness(ind)
		pop.sort(key=lambda ind: ind['fit'], reverse=True)
		pop = copy.deepcopy(pop[:int(len(pop) / 2)]) + copy.deepcopy(pop[:int(len(pop) / 2)])

		best = copy.deepcopy(pop[0])
		print({s: e['name'] for s, e in best.gear.items() if e is not None})
		# print(best)
		for ind in pop:
			if random.random() < mut_chance:
				ind = create_individual()








	# Make a player that can only evolve the gloves they wear
