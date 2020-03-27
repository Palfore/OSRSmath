from osrsmath.model.monsters import Monster, get_monster_data
from osrsmath.model.player import PlayerBuilder, get_equipment_data, get_equipment_by_name
from osrsmath.model.rates import experience_per_hour
from osrsmath.model.experience import combat_level, time_dependent_model_xp
from osrsmath.model.boosts import BoostingSchemes
from osrsmath.model import successful_hits
from collections import defaultdict
from pprint import pprint
import osrsmath.apps.nmz as nmz
import numpy as np
import copy

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

def get_offensive_bonuses(equipment, attack_style):
	assert attack_style in ["crush", "slash", "stab"]
	bonuses = {}
	if equipment['weapon']:
		# Use reciprocal since a greater 1/attack_speed is better,
		# and comparisons are done using >.
		bonuses.update({'reciprocal_attack_speed': 1/equipment['weapon']['attack_speed']})
	bonuses.update({stat:value for stat, value in equipment['equipment'].items() if stat in [
		f"attack_{attack_style}", "melee_strength",
	]})
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


def get_best_set(player_stats: dict, training_skill, boosting_function, defenders, sets, include_shared_xp=True):
	""" Returns the equipment set that provides the highest experience rate for the training_skill.
		@param player_stats: {'attack': 40, ...}
		@param training_skill: 'attack'
		@param sets: [{'cape': 'Fire cape', ...}, {'cape': 'Legends cape', ...}, ...] """
	best = (None, float('-inf'), None)
	for s in sets:
		player = PlayerBuilder(player_stats).equip(s.values()).get()

		# Finds the best stance to train that skill for the given weapon.
		best_set, best_xp_rate, best_stance = best
		for name, stance in player.get_stances().items():
			if stance['experience'] in ([training_skill] + (['shared'] if include_shared_xp else [])):
				player.combat_style = stance['combat_style']
				xp = time_dependent_model_xp(boosting_function(player), defenders, 'MarkovChain')
				# pprint((s, xp))
				if xp > best_xp_rate:
					best = (s, xp, player.combat_style)
	if best[0] == None:
		raise ValueError(f"There was no way to gain {training_skill} experience given these equipment sets: {sets}")
	return best


def get_sets(training_skill, defenders, player_stats, ignore, adjustments, equipment_data):
	reduced_equipment = defaultdict(list)
	for slot, slot_equipment in get_offensive_melee_equipment(equipment_data).items():
		requirements = defaultdict(list)
		for equipment in slot_equipment:
			if equipment['name'] in ignore:
				continue
			if any([equipment['name'].startswith(s) for s in ('Corrupted', 'Zuriel', 'Statius', 'Vesta')]):
				continue
			if equipment['name'] in adjustments:
				equipment['equipment']['requirements'] = adjustments[equipment['name']]
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
	return sets

if __name__ == '__main__':
	# Retrieve Data
	EQD = get_equipment_data()
	monster_data = get_monster_data()
	opponents = nmz.get_opponents(monster_data)

	training_skill = 'attack'
	defenders = {
		'Count Draynor': Monster.from_id(6332),
	}
	ignore = {
		'Spear', # https://oldschool.runescape.wiki/w/Spear_(Last_Man_Standing)
		'Corrupted halberd (perfected)', 'Crystal halberd (perfected)',
		'Corrupted halberd (attuned)', 'Crystal halberd (attuned)',
		'Corrupted halberd (basic)', 'Crystal halberd (basic)',
		'Crystal axe (inactive)',
		'Crystal sceptre',
		'Starter sword',

		'Fighter torso',
		'Infernal max cape', 'Fire max cape', 'Ardougne max cape', 'Infernal cape',
	}
	adjustments = {
		'Gadderhammer': {'attack': 1},  # Not 30 https://oldschool.runescape.wiki/w/Gadderhammer

		'Fire battlestaff': {'attack': 30, 'magic': 30},
		'Water battlestaff': {'attack': 30, 'magic': 30},
		'Air battlestaff': {'attack': 30, 'magic': 30},
		'Earth battlestaff': {'attack': 30, 'magic': 30},
		'Battlestaff': {'attack': 30, 'magic': 30},

		'Ivandis flail': {'attack': 40, 'slayer': 38, 'strength': 40, 'magic': 33},

		'3rd age druidic staff': {'prayer': 65, 'attack': 65}, # Typo: payer, is this a bug in-game?

		'Maple blackjack': {'thieving': 30},
		'Maple blackjack(o)': {'attack': 30, 'thieving': 30},
		'Maple blackjack(d)': {'defence': 30, 'thieving': 30},

		'Western banner 4': {'ranged': 70, 'magic': 64, 'cmb': 100},
		'Western banner 3': {'ranged': 70, 'magic': 64, 'attack': 42, 'defence': 42, 'hitpoints': 42, 'prayer': 22, 'strength': 42, 'slayer': 93},
		'Western banner 2': {'ranged': 30, 'cmb': 70},
		'Wilderness sword 4': {'magic': 96, 'slayer': 83},
		'Wilderness sword 3': {'magic': 66, 'slayer': 68},
		'Wilderness sword 2': {'magic': 60, 'slayer': 50},

		# Need DT and https://forum.tip.it/topic/79597-desert-treasure-lowest-possible-level/page/2/
		'Shadow sword': {'attack': 30, 'strength': 30, 'magic': 51, 'ranged': 42},

		# RFD items are not properly accounted for
		'Spork': {'attack': 10},  # RFD completion
		'Frying pan': {'attack': 20},  # RFD completion
		'Meat tenderiser': {'attack': 46, 'strength': 47, 'defence': 41},  # RFD completion
		'Cleaver': {'attack': 46, 'strength': 47, 'defence': 41},  # RFD completion
		'Spatula': {'attack': 10}, # https://oldschool.runescape.wiki/w/Spatula
		'Skewer': {'attack': 30},
		'Rolling pin': {'attack': 40, 'defence': 41},
		'Katana': {'attack': 40},
		# There might other reqs for these gloves
		'Adamant Gloves': {'defence': 13},
		'Rune gloves': {'defence': 31},
		'Dragon gloves': {'defence': 41},
		'Barrows gloves': {'attack': 46, 'strength': 47, 'defence': 41},
		# https://www.reddit.com/r/2007scape/comments/4gbhzd/barrows_gloves_at_52_cmb/
		# http://i.imgur.com/RXvHBVS.png
	}

	player_stats = {
		'attack': 99,
		'strength': 99,
		'defence': 99,
		'hitpoints': 99,
		'ranged':99,
		'magic': 99,
		'prayer': 99,
		'slayer': 45,
		'mining':99,
		'woodcutting': 99,
		'thieving': 1,
		'agility': 50,
		'fishing': 99,
	}
	for i in [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99]:
		player_stats.update({
			'attack': i,
			'strength': i,
			'defence': i,
		})
		player_stats.update({'cmb': combat_level(player_stats)})
		# If you satisfy a requirement, you can make it None, and choose only from that group!
		sets = get_sets(training_skill, defenders, player_stats, ignore, adjustments, EQD)
		sets = [{ slot: eq for slot, eq in s if eq is not None} for s in sets]
		# pprint(sets)
		s, xp, stance = best = get_best_set(player_stats, 'attack', lambda p: BoostingSchemes(p).overload(), defenders, sets)

		costs = {
			'Gadderhammer': 1_300,
			'Spiked manacles': 1_170_000,
			'Regen bracelet': 2_279_005,
			'Fremennik kilk': 5_332_258,
			'Amulet of torture': 17_054_112,
			'Brimstone ring': 4_106_804,
			'Warrior ring (i)': 42_983,
			'Black scimitar': 1_435,
			'Mithril scimitar': 392,
			'Adamant scimitar': 1_338,
			'Rune Gloves': 6_500,
			'Brine sabre': 149_403,
			'Barrows gloves': 100_000,
			'Berserker helm': 44_264,
			'Granite hammer': 831_247,
			'Obsidian platebody': 1_017_874,
			'Dragon Boots': 302_179,
			'Warrior helm': 41_863,
			'Obsidian platelegs': 821_706,
			'Berserker ring (i)': 2_804_443,
			'Dragon scimitar': 59_568,
			'Bandos chestplate': 20_353_605,
			'Neitiznot faceguard': 27_312_230 + 51_563,
			'Bandos tassets': 29_438_824,
			'Avernic defender': 83_636_792,
			'Abyssal whip': 2_541_568,
			'Primordial boots': 32_007_307,
			'Ferocious gloves': 6_202_804,
			'Blade of saeldor': 137_764_117,
		}

		print(i, xp, sum(costs.get(e, 0) for s, e in s.items()))