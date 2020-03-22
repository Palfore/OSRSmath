from osrsmath.model.monsters import Monster, get_monster_data
from osrsmath.model.player import Player, get_equipment_data, get_equipment_by_name
from osrsmath.model.rates import experience_per_hour
from osrsmath.model import successful_hits
from pprint import pprint
import numpy as np

import osrsmath.apps.nmz as nmz

import copy

from collections import defaultdict


def is_only_melee_weapon(weapon):
	return all(stance['experience'] in ('strength', 'attack', 'defence', 'shared') for stance in weapon['weapon']['stances'])

def has_offensive_melee_bonuses(armour):
	return any(amount > 0 for bonus, amount in armour['equipment'].items() if (bonus in [
		"attack_crush", "attack_slash", "attack_stab", "melee_strength",
	])) and armour['equipable_by_player']
