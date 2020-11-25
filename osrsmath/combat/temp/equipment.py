from typing import Callable, Union
from pathlib import Path
import osrsmath.config as config
from collections import namedtuple
from pprint import pprint
import json

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


class EquipmentPool(object):
	# Singleton https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
	SLOTS = ['2h', 'ammo', 'body', 'cape', 'feet', 'hands', 'head', 'legs', 'neck', 'ring', 'shield', 'weapon']
	__instance = None
	
	def __new__(cls):
		if EquipmentPool.__instance is None:
			EquipmentPool.__instance = object.__new__(cls)
		return EquipmentPool.__instance

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
				equipment[slot] = {ID: item for ID, item in json.load(f).items() if item['equipable_by_player']}
		return equipment

class Bonuses:
	accuracy = ['attack_stab', 'attack_slash', 'attack_crush', 'attack_ranged', 'attack_magic']
	defence = ['defence_stab', 'defence_slash', 'defence_crush', 'defence_ranged', 'defence_magic']
	strength = ['melee_strength', 'ranged_strength', 'magic_damage']
	other = ['prayer']

	normal_bonuses = accuracy + defence + strength + other

	@staticmethod
	def none():
		return Bonuses({
			'equipment': {bonus: 0 for bonus in Bonuses.normal_bonuses},
			'weight': 0,
		})

	@staticmethod
	def by_name(name):
		return Bonuses(EquipmentPool().by_name(name))

	def __init__(self, raw_data: dict, arena=None):
		""" 
		Args:
			raw_data The dictionary from the items.json files.
		"""

		for name in Bonuses.normal_bonuses:
			setattr(self, name, raw_data['equipment'][name])
		self.weight = raw_data['weight']


	def __add__(self, other):
		if not isinstance(other, Bonuses):
			raise ValueError(f'Other must be instance of Bonuses, not {type(other)}.')
		return Bonuses({
			'equipment': {
				bonus: getattr(self, bonus) + getattr(other, bonus) for bonus in Bonuses.normal_bonuses
			},
			'weight': self.weight + other.weight
		})

class Equipment(Bonuses):
	""" Extends the Bonuses class to include meta data. """

	@staticmethod
	def by_name(name):
		return Equipment(EquipmentPool().by_name(name))

	def __init__(self, raw_data: dict):
		""" 
		Args:
			raw_data The dictionary from the items.json files.
		"""
		super().__init__(raw_data)
		self.slot = raw_data['equipment']['slot']
		self.name = raw_data['name'].lower()
		self.id = raw_data['id']
		self.wiki_url = raw_data['wiki_url']
		self.requirements = raw_data['equipment']['requirements']

class Weapon:
	@staticmethod
	def by_name(name):
		return Weapon(EquipmentPool().by_name(name))

	def __init__(self, raw_data: dict=None):
		if raw_data is None:  # Return unarmed
			self.attack_speed = 4
			self.stances = UNARMED
			self.weapon_type = 'unarmed'
		else:
			self.attack_speed = raw_data['weapon']['attack_speed']
			self.stances = {stance['combat_style']: stance for stance in raw_data['weapon']['stances']}
			self.weapon_type = raw_data['weapon']['weapon_type']

		self.attack_interval = self.attack_speed * 0.6


class Loadout:
	""" Only the weapon slot exists, no 2h.
	
	self.stances is a dictionary of the form:
		'attack_name': {
			'attack_style': [aggressive, accurate, defensive, rapid],
			'attack_type': ['stab', 'slash', 'crush', 'ranged', 'magic'],
			'boosts': Not really sure yet,
			'combat_style': same as attack_name,
			'experience': ['attack', 'strength', 'defence', 'shared']
		}, ...
	These are not yet exhaustive options.

	"""

	@property
	def bonuses(self):
		return sum([Equipment(item) for item in self.gear.values() if item is not None], Bonuses.none())

	@property
	def attack_speed(self):
		return Weapon(self.gear['weapon']).attack_speed

	@property
	def attack_interval(self):
		return Weapon(self.gear['weapon']).attack_interval

	@property
	def stances(self):
		return Weapon(self.gear['weapon']).stances

	@property
	def weapon_type(self):
		return Weapon(self.gear['weapon']).weapon_type

	@property
	def equipment(self):
		return {slot: Equipment(item) for slot, item in self.gear.items() if item is not None}

	def __init__(self, worn: list=None):
		self.gear = {slot: None for slot in EquipmentPool.SLOTS if '2h' not in slot}
		self.combat_style = None

		if worn:
			for gear in worn:
				self.equip(gear)

	def wear(self, *names: str):
		""" Equips a piece of equipment by name. """
		pool = EquipmentPool()
		for name in names:
			self.equip(pool.by_name(name))

	def unwear(self, *names: str):
		""" Unequips a piece of equipment by name. """
		for slot, equipment in self.gear.items():
			if equipment is None:
				continue
			if equipment['name'] in names:
				self.unequip(slot)

	def undress(self):
		""" Unequips all equipment. """
		for slot in self.gear:
			self.unequip(slot)
	
	def equip(self, equipment: dict):
		""" Equips a piece of equipment by dict. """
		if isinstance(equipment, str):
			raise ValueError(f"Can't equip non-dict {equipment}. Did you mean to use Equipment.wear()?")
		
		# Unequip slot first
		slot = equipment['equipment']['slot']
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

	def get_names(self):
		""" Returns a list of the worn equipment names. """
		return [e['name'] for e in self.gear.values() if e]



if __name__ == '__main__':
	names = ['Dragon scimitar', 'Occult necklace', 'Bandos chestplate', "Green d'hide chaps"]
	# equipment = map(Equipment.by_name, names)
	# bonuses = sum(equipment, Bonuses.none())
	# pprint(bonuses.__dict__)

	loadout = Loadout()
	loadout.wear(*names)
	pprint(loadout.bonuses.__dict__)
	pprint(loadout.attack_speed)
	pprint(loadout.attack_interval)
	pprint(loadout.stances)
	pprint(loadout.weapon_type)