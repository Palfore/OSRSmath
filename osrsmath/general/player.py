import osrsmath.config as config
from typing import Dict, List
from pathlib import Path
import json

class Player:
	def __init__(self, levels: Dict[str, int]):
		self.levels = levels
		self.equipment = Equipment()


class Equipment:
	""" Only the weapon slot exists, no 2h. """
	UNARMED = {
		'punch': {
			'attack_style': 'accurate',
			'attack_type': 'crush',
			'boosts': None,
			'combat_style': 'punch',
			'experience': 'attack'
		},
		'kick': {
			'attack_style': 'aggressive',
			'attack_type': 'crush',
			'boosts': None,
			'combat_style': 'kick',
			'experience': 'strength'
		},
		'block': {
			'attack_style': 'defensive',
			'attack_type': 'crush',
			'boosts': None,
			'combat_style': 'block',
			'experience': 'defence'
		},
	}

	def __init__(self, worn: list=None):
		self.gear = {slot: None for slot in EquipmentPool.SLOTS if '2h' not in slot}
		self.combat_style = None
		if worn:
			for gear in worn:
				self.equip(gear)

	def wear(self, *names: str):
		""" Equips a piece of equipment by name. """
		pool = EquipmentPoolFiltered()
		for name in names:
			self.equip(pool.by_name(name))

	def undress(self):
		""" Unequips all equipment. """
		for slot in self.gear:
			self.unequip(slot)
	
	def equip(self, equipment: dict):
		""" Equips a piece of equipment by slot. """
		if isinstance(equipment, str):
			raise ValueError(f"Can't equip non-dict {equipment}. Did you mean to use Equipment.wear()?")
		slot = equipment['slot']
		if slot == '2h':
			self.unequip('weapon')
			self.unequip('shield')
			slot = 'weapon'
		elif slot == 'shield' and (self.gear['weapon'] and self.gear['weapon']['slot'] == '2h'):
			self.unequip('weapon')
		assert slot != '2h'
		self.gear[slot] = equipment
	
	def unequip(self, slot):
		""" Unequips a piece of equipment by slot. """
		self.gear[slot] = None

	def get_stances(self):
		""" Returns the player's attack stances. 

		This is a dictionary of the form:
			'attack_name': {
				'attack_style': [aggressive, accurate, defensive, rapid],
				'attack_type': ['stab', 'slash', 'crush', 'ranged', 'magic'],
				'boosts': Not really sure yet,
				'combat_style': same as attack_name,
				'experience': ['attack', 'strength', 'defence', 'shared']
			}, ...

		These are not yet exhaustive options.
		"""
		if self.gear['weapon'] is None:
			return Equipment.UNARMED
		return {stance['combat_style']: stance for stance in self.gear['weapon']['stances']}

	def get_names(self):
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

		overall['stances'] = self.get_stances()
		overall['attack_speed'] = self.gear['weapon']['attack_speed'] if self.gear['weapon'] is not None else 2.4
		overall['weapon_type'] = self.gear['weapon']['weapon_type'] if self.gear['weapon'] is not None else 'unarmed'
		return overall


class GenericPool(object):
	SLOTS = ['2h', 'ammo', 'body', 'cape', 'feet', 'hands', 'head', 'legs', 'neck', 'ring', 'shield', 'weapon']

	def __init__(self):
		self.equipment = EquipmentPool.get_equipment()

	def force_update(self):
		self.get_equipment(force_update=True)

	def by_id(self, ID, slot=None):
		if slot and not slot in self.SLOTS:
			raise ValueError(f"slot is {slot} but must be one of: {SLOTS}")

		for equipment_slot, equipment_slot_data in self.equipment.items():
			if slot is not None and (equipment_slot != slot):
				continue
			for item_id, data in equipment_slot_data.items():
				if item_id == ID:
					return data
		raise ValueError(f"Equipment with id {ID} could not be found.")

	def by_name(self, name, slot=None):
		if slot and not slot in self.SLOTS:
			raise ValueError(f"slot is {slot} but must be one of: {SLOTS}")

		for equipment_slot, equipment_slot_data in self.equipment.items():
			if slot is not None and (equipment_slot != slot):
				continue
			for item_id, data in equipment_slot_data.items():
				if name.lower() == data['name'].lower():
					return data
		raise ValueError(f"Equipment with name '{name}' could not be found.")

	@staticmethod
	def get_equipment(force_update=False):
		equipment = {}
		for slot in EquipmentPool.SLOTS:
			file_name = f'items-{slot}.json'
			file_path = config.resource_path(Path(f"combat/data/{file_name}"))
			if not file_path.exists() or force_update:
				r = requests.get(SLOT_BASE_URL+'/'+file_name)

				with open(file_path, 'w') as f:
					f.write(r.text)

			with open(file_path, 'r') as f:
				equipment[slot] = json.load(f)
		return equipment


class EquipmentPool(GenericPool):
	# Singleton https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
	__instance = None
	def __new__(cls):
		if EquipmentPool.__instance is None:
			EquipmentPool.__instance = object.__new__(cls)
		return EquipmentPool.__instance

class EquipmentPoolFiltered(GenericPool):
	# Singleton https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
	__instance = None
	def __new__(cls):
		if EquipmentPoolFiltered.__instance is None:
			EquipmentPoolFiltered.__instance = object.__new__(cls)
		return EquipmentPoolFiltered.__instance

	def __init__(self):
		super().__init__()
		self.equipment = {
			slot: {
				k: self.filter(v) for k, v in equipment.items()
			} for slot, equipment in self.equipment.items()
		}

	@staticmethod
	def filter(data):
		if data is None:
			return None
		if not all((data['equipable_by_player'], data['equipable'], )):
			# raise ValueError(f"Equipment not equipable by player: {data['name']}, {data['id']}\n{data}")
			return None
		filtered_data = {'name': data['name'], 'id': data['id'], 'wiki_url': data['wiki_url']}
		filtered_data.update(data['equipment'])
		if data['weapon'] is not None:
			filtered_data.update(data['weapon'])
			filtered_data['attack_speed'] *= 0.6  # Convert attack_speed into [attacks/second]
		filtered_data['weight'] = data['weight'] if data['weight'] is not None else 0.0
		return filtered_data


if __name__ == '__main__':
	from pprint import pprint
	# player = Player({'attack': 70, 'strength': 70, 'defence': 70})
	# # player.equipment.wear('Dragon Scimitar')
	# # player.equipment.wear('Ale of the gods')
	# pprint(player.equipment.get_combat_type())


	x = EquipmentPool().by_name('dragon scimitar')
	pprint(x)
	x = EquipmentPoolFiltered().by_name('dragon scimitar')
	pprint(x)