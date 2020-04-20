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

def load_opponent(search_type, value):
	if search_type == 'id':
		return Monster.from_id(value)
	elif search_type == 'name':
		return Monster.from_name(value)
	else:
		raise ValueError(f'The search type must be either "id" or "name", not {search_type}')

def load(file_name, process_opponents=True):
	data = JsonComment().loadf(file_name)
	player_stats = data['player_stats']
	if process_opponents:
		defenders = {}
		for name, (search_type, value) in data['defenders'].items():
			if process_opponents:
				defenders[name] = load_opponent(search_type, value)
	else:
		defenders = data['defenders']
	ignore = data['ignore']
	adjustments = data['adjustments']
	return player_stats, defenders, ignore, adjustments

def is_only_melee_weapon(weapon):
	# return all(stance['experience'] in ('strength', 'attack', 'defence', 'shared') for stance in weapon['weapon']['stances'])
	# This is too restrictive because of staffs!
	# but looking at 'shared' is worse because all magic and ranged items (pretty much) have shared
	# so instead, since we can't handle shared anyway
	# return weapon['weapon']['weapon_type'] not in ('bow', 'grenade', 'crossbow', 'thrown', 'blaster', 'gun')
	return True

def has_offensive_melee_bonuses(armour):
	return any(amount > 0 for bonus, amount in armour['equipment'].items() if (bonus in [
		"attack_crush", "attack_slash", "attack_stab", "melee_strength",
	])) and armour['equipable_by_player']

def get_offensive_melee_equipment(equipment_data):
	# Reduce the equipment to only those that have a) offensive bonuses, b) melee bonuses
	# Filter for only melee weapons since other attack styles aren't handled yet
	# Also only equipment that gives offensive bonuses, since that is what we're optimizing
	offensive_equipment = defaultdict(list)
	for slot, equipment in equipment_data.items():
		if slot == "weapon" or slot ==  "2h":
			for weapon in equipment.values():
				if is_only_melee_weapon(weapon) and has_offensive_melee_bonuses(weapon):
					offensive_equipment[slot].append(weapon)
		else:
			for armour in equipment.values():
				if has_offensive_melee_bonuses(armour):
					offensive_equipment[slot].append(armour)
	return offensive_equipment

def get_offensive_bonuses(equipment, attack_style=None):
	assert attack_style in ["crush", "slash", "stab"]
	bonuses = {}
	if equipment['weapon']:
		# Use reciprocal since a greater 1/attack_speed is better,
		# and comparisons are done using >.
		bonuses.update({'reciprocal_attack_speed': 1/equipment['weapon']['attack_speed']})

	if attack_style:
		allowed = [f"attack_{attack_style}", "melee_strength"]
	else:
		allowed = ["attack_crush", "attack_stab", "attack_slash", "melee_strength"]

	bonuses.update({stat:value for stat, value in equipment['equipment'].items() if stat in allowed})
	return bonuses

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

def meets_requirements(player_stats, equipment):
	for stat, req in equipment['equipment']['requirements'].items():
		if stat not in player_stats:
			raise ValueError(f"Supply your {stat} level to check {equipment['name']} for: {equipment['equipment']['requirements']}")
		if player_stats[stat] < req:
			return False
	return True

def get_sets(player_stats, defenders, ignore, adjustments, equipment_data=get_equipment_data(), progress_callback=None):
	reduced_equipment = defaultdict(list)
	items = get_offensive_melee_equipment(equipment_data).items()
	for i, (slot, slot_equipment) in enumerate(items, 1):
		if progress_callback:
			progress_callback(100*i / len(items))
		requirements = defaultdict(list)
		for equipment in slot_equipment:
			if equipment['name'] in ignore:
				continue
			if any([equipment['name'].startswith(s) for s in ('Corrupted', 'Zuriel', 'Statius', 'Vesta')]):
				continue
			if equipment['name'] in adjustments:
				equipment['equipment']['requirements'] = adjustments[equipment['name']]

			# If you satisfy a requirement, you can make it None, and choose only from that group!
			if equipment['equipment']['requirements']:
				if meets_requirements(player_stats, equipment):
					equipment['equipment']['requirements'] = None
				else:
					continue

			# https://stackoverflow.com/questions/1600591/using-a-python-dictionary-as-a-key-non-nested
			reqs = tuple(sorted(equipment['equipment']['requirements'].items())) if equipment['equipment']['requirements'] else None
			stats = get_offensive_bonuses(equipment, 'slash')
			if stats not in [s for n, s, _ in requirements[reqs]]:
				requirements[reqs].append((equipment['name'], stats, equipment))

		final = defaultdict(list)
		for req, eqs in requirements.items():
			for e in eqs:
				# Add so long as not everyone is better than you.
				if all([not is_better(E, e[1]) for n, E, _ in eqs]):
					final[req].append(e)

		reduced_equipment[slot] = []
		for r, es in final.items():
			assert r is None
			for e in es:
				reduced_equipment[slot].append(e[0])
		if not reduced_equipment[slot]:
			reduced_equipment[slot].append(None)


	import itertools
	reduced_equipment = ([[(slot, e) for e in eqs] for slot, eqs in reduced_equipment.items()])
	sets = list(itertools.product(*list(reduced_equipment)[:-2]))
	sets += list(itertools.product(*list(reduced_equipment)[1:]))
	return [{ slot: eq for slot, eq in s if eq is not None} for s in sets]


def eval_set(player_stats: dict, training_skill, states, defenders, s, include_shared_xp=True):
	player = PlayerBuilder(player_stats).equip(s.values()).get()

	# Finds the best stance to train that skill for the given weapon.
	best_set, best_xp_rate, best_stance = best = (None, float('-inf'), None)
	for name, stance in player.get_stances().items():
		if stance['experience'] in ([training_skill] + (['shared'] if include_shared_xp else [])):
			player.combat_style = stance['combat_style']
			xp = xp_rate(
				stance['attack_type'],
				player.get_stats()['attack_speed'],
				states(player),
				defenders,
				'MarkovChain'
			)
			if xp > best[1]:
				best = (s, xp, player.combat_style)
	return best

def get_best_set(player_stats: dict, training_skill, states, defenders, sets, include_shared_xp=True, progress_callback=None):
	""" Returns the equipment set that provides the highest experience rate for the training_skill.
		@param player_stats: {'attack': 40, ...}
		@param training_skill: 'attack'
		@param sets: [{'cape': 'Fire cape', ...}, {'cape': 'Legends cape', ...}, ...] """
	best = (None, float('-inf'), None)
	for i, s in enumerate(sets, 1):
		if progress_callback:
			progress_callback(100*i/len(sets))
		_, xp, combat_syle = eval_set(player_stats, training_skill, states, defenders, s, include_shared_xp)
		if xp > best[1]:
			best = (s, xp, combat_syle)

	if best[0] == None:
		raise ValueError(f"There was no way to gain {training_skill} experience given these equipment sets: {sets}")
	return best
