""" This file provides an interface for playable characters through the Player class.
	In addition, several function are provided to load details about relevant equipment.

	Note that at this point, there are a few assumptions / restrictions:
		1) Assume Melee combat. For simplicity, melee combat is first to be modeled.
		      later on, the other combat styles will be added.
"""

from pprint import pprint
from pathlib import Path
import requests
import json
import os

import osrsmath.config as config
import osrsmath.combat.damage as damage
import osrsmath.combat.boosts as boosts
import osrsmath.combat.experience as experience

SLOT_BASE_URL = "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/docs/items-json-slot"
SLOTS = ['2h', 'ammo', 'body', 'cape', 'feet', 'hands', 'head', 'legs', 'neck', 'ring', 'shield', 'weapon']

class PlayerBuilder:
	def __init__(self, stats, equipment_data=None):
		self.player = Player(stats)
		self.equipment_data = get_equipment_data() if equipment_data is None else equipment_data

	def equip(self, equipment):
		if type(equipment) == str:
			self.player.equip_by_name(equipment, self.equipment_data)
		else:
			for e in equipment:
				self.player.equip_by_name(e, self.equipment_data)
		return self

	def get(self):
		return self.player

class Player:
	def __init__(self, levels):
		self.levels = levels
		self.current_health = self.levels['current_health'] if 'current_health' in self.levels else None
		self.gear = {slot: None for slot in SLOTS if '2h' not in slot}
		self.combat_style = None

	### EQUIPMENT ##################################################################################
	def equip(self, equipment):
		slot = equipment['slot']
		if slot == '2h':
			self.unequip('weapon')
			self.unequip('shield')
			slot = 'weapon'
		elif slot == 'shield' and (self.gear['weapon'] and self.gear['weapon']['slot'] == '2h'):
			self.unequip('weapon')
		assert slot != '2h'
		self.gear[slot] = equipment

	def equip_by_id(self, id, equipment_data=None):
		self.equip(filter_equipment(get_equipment_by_id(id, slot=None, equipment_data=equipment_data)))

	def equip_by_name(self, name, equipment_data=None):
		self.equip(filter_equipment(get_equipment_by_name(name, slot=None, equipment_data=equipment_data)))

	def unequip(self, slot):
		self.gear[slot] = None

	### GETTERS ##################################################################################
	def get_stances(self):
		return {stance['combat_style']: stance for stance in self.gear['weapon']['stances']}

	def get_combat_type(self):
		""" Returns Melee, Ranged, or Magic based on experience gained. """
		if self.combat_style is None:
			return None
		if 'ranged' in self.get_stances()[self.combat_style]['experience']:
			return 'Ranged'
		if 'magic' in self.get_stances()[self.combat_style]['experience']:
			return 'Magic'
		return {
			'stab': 'Melee',
			'slash': 'Melee',
			'crush': 'Melee',
			'ranged': 'Ranged',
			'magic': 'Magic',
		}[self.get_stances()[self.combat_style]['attack_type']]

	def get_equipment_names(self):
		""" Returns a list of the worn equipment names. """
		return [e['name'] for e in self.gear.values() if e]

	def get_stats(self):
		overall = {}
		for slot, equipment in self.gear.items():
			assert slot != '2h'  # 2h slot is not used, 2h's go into weapon slot.
			if equipment is None:
				continue
			for stat, value in equipment.items():
				if stat in ('name', 'requirements', 'slot', 'id', 'stances', 'attack_speed', 'weapon_type'):
					continue
				if stat in overall:
					overall[stat] += value
				else:
					overall[stat] = value
		overall['stances'] = self.gear['weapon']['stances']
		overall['attack_speed'] = self.gear['weapon']['attack_speed']
		overall['weapon_type'] = self.gear['weapon']['weapon_type']
		return overall


	### DAMAGE ##################################################################################
	def can_attack(self):
		pass

	def get_damage_parameters(self):
		stats = self.get_stats()
		stances = self.get_stances()
		if self.get_combat_type() == 'Melee':
			return {
				'offensive_equipment_bonus': stats['melee_strength'],
				'offensive_skill': 'strength',
				'offensive_stance_bonus': {'aggressive': 3, 'controlled': 1}.get(stances[self.combat_style]['attack_style'], 0),
				'accuracy_equipment_bonus': stats['attack_' + stances[self.combat_style]['attack_type']],
				'accuracy_skill': 'attack',
				'accuracy_stance_bonus': {'accurate': 3, 'controlled':1}.get(stances[self.combat_style]['attack_style'], 0),
			}
		elif self.get_combat_type() == 'Ranged':
			return {
				'offensive_equipment_bonus': stats['ranged_strength'],
				'offensive_skill': 'ranged',
				'offensive_stance_bonus': {'accurate': 3}.get(stances[self.combat_style]['attack_style'], 0),
				'accuracy_equipment_bonus': stats['attack_ranged'],
				'accuracy_skill': 'ranged',
				'accuracy_stance_bonus': {'accurate': 3}.get(stances[self.combat_style]['attack_style'], 0),
			}
		elif self.get_combat_type() == 'Magic':
			raise ValueError("Magic is not supported")
		else:
			raise ValueError("Could not identify combat type")


	def get_max_hit(self, potion, prayer):
		dmg = self.get_damage_parameters()

		other = boosts.Equipment.none()
		other.update(boosts.other(self.get_equipment_names(), self))
		special_attack_bonus = 1  # Special attacks are not implemented
		multipler = 1  # Ignoring flooring order, since there is no official documentation
		return damage.Standard().max_hit(
			dmg['offensive_equipment_bonus'],
			self.levels[dmg['offensive_skill']],
			potion(self.levels[dmg['offensive_skill']]),
			prayer(dmg['offensive_skill']),
			other[dmg['offensive_skill']],
			dmg['offensive_stance_bonus'],
			1, multipler
		)

	def get_attack_roll(self, potion, prayer):
		dmg = self.get_damage_parameters()
		stances = self.get_stances()

		other = boosts.Equipment.none()
		other.update(boosts.other(self.get_equipment_names(), self))
		multipler = 1  # Ignoring flooring order, since there is no official documentation

		return damage.Standard().max_attack_roll(
			dmg['accuracy_equipment_bonus'],
			self.levels[dmg['accuracy_skill']],
			potion(self.levels[dmg['accuracy_skill']]),
			prayer(dmg['accuracy_skill']),
			other[dmg['accuracy_skill']],
			dmg['accuracy_stance_bonus'],
			multipler
		)

	def get_defence_roll(self, attacker_attack_type, potion, prayer, multipler, using_special=False):
		assert not using_special, "Special attacks are not implemented"
		stats = self.get_stats()
		stances = self.get_stances()

		other = boosts.Equipment.none()
		other.update(boosts.other(self.get_equipment_names()))
		multipler = 1  # Ignoring flooring order, since there is no official documentation
		if self.get_combat_type() in ('Melee', 'Ranged'):
			return damage.Standard().max_defence_roll(
				stats['defence_' + attacker_attack_type],
				self.levels['defence'],
				potion(self.levels['defence']),
				prayer('defence'),
				other['defence'],
				{'longrange': 3, 'defensive': 3, 'controlled': 1,}.get(stances[self.combat_style]['attack_style'], 0),
				multipler
			)
		elif self.get_combat_type() == 'Magic':
			raise ValueError("Magic is not supported")
		else:
			raise ValueError("Could not identify combat type")

	@staticmethod
	def get_accuracy(attack_roll, opponent_defence_roll):
		return damage.accuracy(attack_roll, opponent_defence_roll)

	### EXPERIENCE ##################################################################################
	def xp_rate(self, states, opponents):
		attack_type = self.get_stances()[self.combat_style]['attack_type']
		if attack_type is None:
			attack_type = self.get_combat_type().lower()

		speed_bonus = -0.6 if self.get_stances()[self.combat_style]['boosts'] == "attack speed by 1 tick" else 0
		return experience.xp_rate(
			attack_type,
			self.get_stats()['attack_speed'] + speed_bonus,
			states, opponents
		)

	def time_to_level(self, states, opponents):
		training = self.get_stances()[self.combat_style]['experience']
		if training == 'shared':
			raise ValueError("Only direct experience is allowed, not shared")

		return experience.time_to_level(self.levels[training], self.xp_rate(states, opponents))

	### OTHER ##################################################################################
	def print(self):
		padding = max(len(slot) for slot in self.gear.keys())
		print("Levels:")
		for stat, level in self.levels.items():
			print(f"\t{stat}: {level}")

		print("Equipment:")
		for slot, equipment in self.gear.items():
			print(f"\t{slot:{padding}}: {equipment['name'] if equipment else None}")

		print("Stats:")
		for stat, value in self.get_stats().items():
			if stat in ('stances', 'weapon_type'):
				continue
			print(f"\t{stat}: {value}")

		print("Attack Stances:", ', '.join([f"[{k}: {v['attack_type']}, {v['experience']}]" for k, v in self.get_stances().items()]))
		print(f"Currently Using {self.combat_style}", end=' ' if self.combat_style else '\n')
		if self.combat_style:
			print(f"which trains {self.get_stances()[self.combat_style]['experience']} ({self.get_combat_type()})")


def get_equipment_slot_data(slot, force_update=False):
	file_name = f'items-{slot}.json'
	file_path = config.resource_path(Path(f"combat/data/{file_name}"))
	if not file_path.exists() or force_update:
		r = requests.get(SLOT_BASE_URL+'/'+file_name)

		with open(file_path, 'w') as f:
			f.write(r.text)

	with open(file_path, 'r') as f:
		return json.load(f)

def get_equipment_data(force_update=False):
	data = {}
	for slot in SLOTS:
		data[slot] = get_equipment_slot_data(slot, force_update=force_update)
	return data

def get_equipment_by_id(id, slot=None, equipment_data=None):
	if equipment_data is None:
		equipment_data = get_equipment_data()

	for equipment_slot, equipment_slot_data in equipment_data.items():
		if slot is not None and (equipment_slot != slot):
			continue
		for item_id, data in equipment_slot_data.items():
			if item_id == id:
				return data
	raise ValueError(f"Equipment with id {id} could not be found.")

def get_equipment_by_name(name, slot=None, equipment_data=None):
	if slot:
		assert slot in SLOTS, f"slot is {slot} but must be one of: {SLOTS}"
	if equipment_data is None:
		equipment_data = get_equipment_data()
	for equipment_slot, equipment_slot_data in equipment_data.items():
		if slot is not None and (equipment_slot != slot):
			continue
		for item_id, data in equipment_slot_data.items():
			if name.lower() == data['name'].lower():
				return data
	raise ValueError(f"Equipment with name '{name}' could not be found.")

def filter_equipment(data):
	if data is None:
		return None
	if not all((data['equipable_by_player'], data['equipable'], )):
		# raise ValueError(f"Equipment not equipable by player: {data['name']}, {data['id']}\n{data}")
		return None
	filtered_data = {'name': data['name'], 'id': data['id']}
	filtered_data.update(data['equipment'])
	if data['weapon'] is not None:
		filtered_data.update(data['weapon'])
		filtered_data['attack_speed'] *= 0.6  # Convert attack_speed into [attacks/second]
	filtered_data['weight'] = data['weight'] if data['weight'] is not None else 0.0
	return filtered_data

if __name__ == '__main__':
	from monsters import Monster
	equipment_data = get_equipment_data()

	attacker = Player({'attack': 70, 'strength': 85, 'defence': 70, 'prayer': 56, 'hitpoints': 79, 'magic': 71, 'ranged': 70})
	attacker.equip_by_name("Dragon Scimitar")
	attacker.equip_by_name("Dharok's helm")
	attacker.equip_by_name("Dharok's platebody")
	attacker.equip_by_name("Dharok's platelegs")
	attacker.equip_by_name("Dragon Boots")
	attacker.equip_by_name("Holy Blessing")
	attacker.equip_by_name("Barrows Gloves")
	attacker.equip_by_name("Dragon Defender")
	attacker.equip_by_name("Berserker Ring (i)")
	attacker.equip_by_name("Amulet of Fury")
	attacker.equip_by_name("Fire Cape")
	attacker.combat_style = 'slash'
	m = attacker.get_max_hit(0, 1, 1)
	A = attacker.get_attack_roll(0, 1, 1, 1)

	defender = Monster.from_name("Black Demon (hard)")
	D = defender.get_defence_roll(attacker.get_stances()[attacker.combat_style]['attack_type'], 0, 1, 1, 1)
	a = defender.get_accuracy(A, D)
	print(m, A, D, a)
	exit()

	# Check that all equipable items work (don't crash)
	attacker = Player({})
	for slot, data in equipment_data.items():
		for key in data.keys():
			item = filter_equipment(get_equipment_by_id(key, equipment_data=equipment_data))
			if item is None:
				continue
			attacker.equip(item)
			attacker.get_stats()
	pprint(attacker.get_stats())
	pprint(attacker.gear)