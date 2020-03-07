""" This file provides an interface for playable characters through the Player class.
	In addition, several function are provided to load details about relevant equipment.

	Note that at this point, there are a few assumptions / restrictions:
		1) Assume Melee combat. For simplicity, melee combat is first to be modeled.
		      later on, the other combat styles will be added.
"""

from pprint import pprint
import requests
import json
import os

import osrsmath.config as config
import osrsmath.model.damage as damage

SLOT_BASE_URL = "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/docs/items-json-slot"
SLOTS = ['2h', 'ammo', 'body', 'cape', 'feet', 'hands', 'head', 'legs', 'neck', 'ring', 'shield', 'weapon']

def get_equipment_slot_data(slot, force_update=False):
	file_name = f'items-{slot}.json'
	file_path = os.path.join(config.DATA_PATH, file_name)
	if not os.path.exists(file_path) or force_update:
		r = requests.get(os.path.join(SLOT_BASE_URL, file_name))

		with open(file_path, 'w') as f:
			f.write(r.text)

	with open(file_path, 'r') as f:
		return json.load(f)

def get_equipment_data(force_update=False):
	data = {}
	for slot in SLOTS:
		data[slot] = get_equipment_slot_data(slot)
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
	if equipment_data is None:
		equipment_data = get_equipment_data()
	for equipment_slot, equipment_slot_data in equipment_data.items():
		if slot is not None and (equipment_slot != slot):
			continue
		for item_id, data in equipment_slot_data.items():
			if name.lower() == data['name'].lower():
				return data
	raise ValueError(f"Equipment with name {name} could not be found.")

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

class Player:
	def __init__(self, levels):
		self.levels = levels
		self.gear = {slot: None for slot in SLOTS if '2h' not in slot}
		self.combat_style = None

	def get_stances(self):
		return {stance['combat_style']: stance for stance in self.gear['weapon']['stances']}

	def equip_by_id(self, id, equipment_data=None):
		self.equip(filter_equipment(get_equipment_by_id(id, slot=None, equipment_data=equipment_data)))

	def equip_by_name(self, name, equipment_data=None):
		self.equip(filter_equipment(get_equipment_by_name(name, slot=None, equipment_data=equipment_data)))

	def equip(self, equipment):
		slot = equipment['slot']
		if slot == '2h':
			self.unequip('weapon')
			self.unequip('shield')
			slot = 'weapon'
		elif slot == 'shield' and self.gear['weapon']['slot'] == '2h':
			self.unequip('weapon')
		assert slot != '2h'
		self.gear[slot] = equipment

	def unequip(self, slot):
		self.gear[slot] = None

	def get_stats(self):
		overall = {}
		for slot, equipment in self.gear.items():
			assert slot != '2h'
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

	def get_max_hit(self, strength_potion_boost, strength_prayer_boost, strength_other_boost, multipler, using_special=False):
		assert not using_special, "Special attacks are not implemented"
		# WARNING: ONLY HANDLES (AND ASSUMES MELEE COMBAT!)
		stats = self.get_stats()
		stances = self.get_stances()
		return damage.Melee().max_hit(
			stats['melee_strength'],
			self.levels['strength'],
			strength_potion_boost,
			strength_prayer_boost,
			strength_other_boost,
			{'aggressive': 3, 'controlled': 1,}.get(stances[self.combat_style]['attack_style'], 0),
			1,  # Special attack multiplier
			multipler
		)

	def get_attack_roll(self, attack_potion_boost, attack_prayer_boost, attack_other_boost, multipler, using_special=False):
		assert not using_special, "Special attacks are not implemented"
		stats = self.get_stats()
		stances = self.get_stances()
		attack_type = stances[self.combat_style]['attack_type']
		return damage.Melee().max_attack_roll(
			stats['attack_' + stances[self.combat_style]['attack_type']],
			self.levels['attack'],
			attack_potion_boost,
			attack_prayer_boost,
			attack_other_boost,
			{'accurate': 3, 'controlled': 1,}.get(stances[self.combat_style]['attack_style'], 0),
			multipler
		)


	def get_defence_roll(self, attacker_attack_type, defence_potion_boost, defence_prayer_boost, defence_other_boost, multipler, using_special=False):
		assert not using_special, "Special attacks are not implemented"
		stats = self.get_stats()
		stances = self.get_stances()
		return damage.Melee().max_defence_roll(
			stats['defence_' + attacker_attack_type],
			self.levels['defence'],
			defence_potion_boost,
			defence_prayer_boost,
			defence_other_boost,
			{'defensive': 3, 'controlled': 1,}.get(stances[self.combat_style]['attack_style'], 0),
			multipler
		)

	@staticmethod
	def get_accuracy(attack_roll, opponent_defence_roll):
		return damage.Melee().accuracy(attack_roll, opponent_defence_roll)

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