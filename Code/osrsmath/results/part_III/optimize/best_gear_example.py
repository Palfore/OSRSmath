# def get_equipment_that_has_offensive_bonuses(player_stats, ignore, equipment_data=get_equipment_data()):
# 	e = defaultdict(list)
# 	for slot, slot_equipment in equipment_data.items():
# 		for ID, equipment in slot_equipment.items():
# 			if equipment['name'] in ignore:
# 				continue
# 			if any([equipment['name'].startswith(s) for s in ('Corrupted', 'Zuriel', 'Statius', 'Vesta')]):
# 				continue
# 			if any(equipment['equipment'][stat] > 0 for stat in ('attack_stab', 'attack_crush', 'attack_slash', 'attack_ranged', 'attack_magic', 'ranged_strength', 'magic_damage', 'melee_strength')):
# 				e[slot].append(equipment)
# 	return e

from jsoncomment import JsonComment
from osrsmath.apps.optimize import get_sets, eval_set, load, get_best_set
from osrsmath.model.player import get_equipment_data
from osrsmath.model.experience import combat_level
from osrsmath.model.monsters import Monster
from osrsmath.model.boosts import BoostingSchemes, Prayers, Potions
from pprint import pprint
import sys
import os


from jsoncomment import JsonComment
from osrsmath.model.monsters import Monster, get_monster_data
from osrsmath.model.player import PlayerBuilder, get_equipment_data, get_equipment_by_name
from osrsmath.model.rates import experience_per_hour
from osrsmath.model.experience import combat_level, xp_rate
from osrsmath.model.boosts import BoostingSchemes
from osrsmath.model import successful_hits
from collections import defaultdict
from pprint import pprint
import osrsmath.apps.nmz as nmz
import numpy as np
import copy

weapon_type = 'weapon'

def get_stances_that_can_train(weapon, skill, allow_shared=True):
	""" Returns the stances (by combat_style) that the {weapon} can train the {skill} with. """
	stances = []
	for stance in weapon['weapon']['stances']:
		s = stance['experience']

		# Stances come in 4 flavors:
		#     1) attack, strength, defence, magic, ranged
		#     2) "magic and defence", "ranged and defence"
		#     3) none
		#     4) shared
		# The first 2 can be identifies with the '==' or 'in' operators, respectively.
		# The 3rd is simply ignored. Since the 2nd accounts for both magic and ranged,
		# 'shared' is specifically melee.
		assert s in ('attack', 'strength', 'defence', 'magic', 'ranged', 'magic and defence', 'ranged and defence', 'none', 'shared'), s
		if skill == s:
			stances.append(stance['combat_style'])
		elif allow_shared:
			if skill in s:
				stances.append(stance['combat_style'])
			elif s == 'shared':
				assert stance['attack_type'] in ('stab', 'crush', 'slash'), stance['attack_type']
				if skill in ('attack', 'strength', 'defence'):
					stances.append(stance['combat_style'])
	return stances

def get_attack_types_that_train(weapon, skill, allow_shared=True):
	stances_dict = {s['combat_style']: s for s in weapon['weapon']['stances']}
	stances = get_stances_that_can_train(weapon, skill, allow_shared)

	possible_attack_types = set()
	for stance in stances:
		stance = stances_dict[stance]
		if 'magic' in stance['experience']:
			possible_attack_types.add('attack_magic')
		elif 'ranged' in stance['experience']:
			possible_attack_types.add('attack_ranged')
		else:
			possible_attack_types.add('attack_' + stance['attack_type'])
	return possible_attack_types

def get_weapons_that_can_train(skill, allow_shared=True, equipment_data=get_equipment_data()):
	assert skill in ('attack', 'strength', 'defence', 'magic', 'ranged')
	weapons = []
	for ID, weapon in list(equipment_data[weapon_type].items()):
		assert weapon['equipable_by_player'] and weapon['weapon']
		if get_stances_that_can_train(weapon, skill, allow_shared):
			weapons.append(weapon)
	return weapons

def get_weapons_that_have_training_bonuses(skill, allow_shared=True, equipment=get_equipment_data()):
	weapons = []
	for weapon in get_weapons_that_can_train(skill, allow_shared, equipment):
		possible_attack_types = get_attack_types_that_train(weapon, skill, allow_shared)
		assert possible_attack_types
		# Could also include weapon['weapon']['attack_speed'] < 4 for weapons faster than unarmed.
		# but this would only be additionally added if they have no relevant bonuses.
		if any(weapon['equipment'][attack_type] > 0 for attack_type in possible_attack_types):
			weapons.append(weapon)
	return weapons

def meets_requirements(player_stats, equipment):
	if equipment['equipment']['requirements'] is None:
		return True
	for stat, req in equipment['equipment']['requirements'].items():
		if stat not in player_stats:
			raise ValueError(f"Supply your {stat} level to check {equipment['name']} for: {equipment['equipment']['requirements']}")
		if player_stats[stat] < req:
			return False
	return True

def get_equipable(equipment, player_stats, ignore, adjustments):
	equipable = []
	for eq in equipment:
		if eq['name'] in ignore:
			continue
		if any([eq['name'].startswith(s) for s in ('Corrupted', 'Zuriel', 'Statius', 'Vesta')]):
			continue
		if eq['name'] in adjustments:
			eq['equipment']['requirements'] = adjustments[eq['name']]
		if meets_requirements(player_stats, eq):
			equipable.append(eq)
	return equipable

def is_better(A, B):
	""" Is A absolutely better than B?
		@param A Equipment stats eg: {'attack_crush': 53, ...}
		@param B Equipment stats """
	assert list(A.keys()) == list(B.keys())
	if list(A.values()) == list(B.values()):
		return False
	for a, b in zip(list(A.values()), list(B.values())):
		if b > a:
			return False
	return True

def reduce_bonuses(equipment, attack_type):
	bonuses = [attack_type]
	if 'magic' in attack_type:
		bonuses.append('magic_damage')
	elif 'ranged' in attack_type:
		bonuses.append('ranged_strength')
	else:
		bonuses.append('melee_strength')
	reduced = {b: v for b, v in equipment['equipment'].items() if b in bonuses}
	reduced['reciprocal_attack_speed'] = 1/equipment['weapon']['attack_speed']
	return reduced

def get_best_options(skill, player_stats, ignore, adjustments, allow_shared=True):
	weapons = get_equipable(get_weapons_that_have_training_bonuses(skill, allow_shared), player_stats, ignore, adjustments)

	# Sort equipment by attack bonus required to train
	weapons_by_attack_type = defaultdict(list)
	for weapon in weapons:
		for attack_type in get_attack_types_that_train(weapon, skill, allow_shared):
			weapons_by_attack_type[attack_type].append(weapon)

	# Then only select the strictly better set of those.
	best_by_attack_type = defaultdict(list)
	for attack_type, weapons in weapons_by_attack_type.items():
		for weapon in weapons:
			# So long as not everyone is better than you.
			if all([not is_better(
						reduce_bonuses(w, attack_type),
						reduce_bonuses(weapon, attack_type)
					) for w in weapons]) and (  # And your stats aren't already included
						reduce_bonuses(weapon, attack_type) not in [
							reduce_bonuses(e, attack_type) for e in best_by_attack_type[attack_type]
						]
					):
				best_by_attack_type[attack_type].append(weapon)
	return best_by_attack_type



if __name__ == '__main__':
	player_stats, defenders, ignore, adjustments = load("settings.json")
	player_stats.update({
		'attack': 60,
		'strength': 60,
		'defence': 50,
		'hitpoints': 50,
		'magic': 50,
		'ranged': 50,
		'prayer': 43
	})
	player_stats.update({'cmb': combat_level(player_stats)})
	ignore.extend([
		'Amulet of torture',
		'Amulet of torture (or)',
		'Fighter torso',
		'Fire cape',
	])

	# e = get_equipable(get_weapons_that_have_training_bonuses('attack', True), player_stats, ignore, adjustments)
	e = get_best_options('defence', player_stats, ignore, adjustments, allow_shared=False)
	pprint([(e, [w['name'] for w in ws]) for e, ws in e.items()])
	# print(len(e))


	# I now have a function that will give me the best weapons possible for a given attack_type for training something
	# So "train attack using slash" gives me a weapon set.
	# For each attack_type, I can try on the equipment that gives the best bonuses.
	# ie for attack_stab, what helmets give the best bonus? (considering that str might also go up)
	# At the end of the day, the user should be able to click on a suggest, and say "what are alternatives"


	# best_set = get_best_set(player_stats, 'attack',
	# 	lambda p: BoostingSchemes(p, Prayers.none).constant(Potions.overload),
	# 	defenders, get_sets(player_stats, defenders, ignore, adjustments), include_shared_xp=True
	# )
	# pprint(best_set)
