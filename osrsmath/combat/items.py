from pathlib import Path
import osrsmath.config as config
import json
from copy import deepcopy

def get_combat_class(stance):
	""" Returns one of ranged, magic, melee, or None if the stance cannot do damage. """
	if stance['experience'] is None:
		return None  # No combat class, since weapon cannot do damage
	if 'ranged' in stance['experience']:
		return 'ranged'
	elif 'magic' in stance['experience']:
		return 'magic'
	elif any(stance['attack_type'] == melee_type for melee_type in ['stab', 'slash', 'crush']):
		return 'melee'
	else:
		raise LogicError(f"Something went wrong determining combat class for stance: {stance}")

class ItemDatabase:
	SLOTS = ['2h', 'ammo', 'body', 'cape', 'feet', 'hands', 'head', 'legs', 'neck', 'ring', 'shield', 'weapon']

	def __init__(self):
		self.items = ItemDatabase.get_equipment()
		self.IDs = {item['name']: ID for ID, item in self.items.items()}
		self.slots = {slot: [] for slot in self.SLOTS}
		for ID, item in self.items.items():
			self.slots[item['equipment']['slot']].append(ID)

	def get_slot(self, slot: str):
		return self.slots[slot]

	def find(self, name: str):
		if name not in self.IDs:
			raise KeyError(f'Could not find item named "{name}" in the item database.')
		return self.get(self.IDs[name])
		
	def get(self, ID: int):
		if ID not in self.items:
			raise KeyError(f'Could not find item with id {ID} in the item database.')
		return self.items[ID]

	@staticmethod
	def create_dummy(equipment, weapon=None, name="dummy", ID=None, weight=0.0):
		return {
			'name': name,
			'id': ID,
			'weight': weight,
			'wiki_url': "",
			"equipment": equipment,
			"weapon": weapon,
		}

	@staticmethod
	def get_equipment(force_update=False):
		def filter(i):
			partial = {k: v for k, v in i.items() if k in [
				'name', 'id', 'weight', 'wiki_url', 'equipment', 'weapon'
			]}
			
			## Convert stances from a list to a dictionary
			if partial['weapon'] is not None:
				partial['weapon']['stances'] = {
					s['combat_style']: s for s in partial['weapon']['stances']
				}
			
			## Corrections
			# For some reason, "Mithril crossbow" is incorrectly called "Mith crossbow".
			partial['name'] = "Mithril crossbow" if partial['name'] == 'Mith crossbow' else partial['name']
			
			# Salamander's incorrectly have None as the attack style
			if partial['name'] in ["Black salamander", "Red salamander", "Orange salamander", "Swamp lizard"]:
				partial['weapon']['stances']['scorch']['attack_style'] = "aggressive"
				partial['weapon']['stances']['scorch']['attack_style'] = "ranged"
				partial['weapon']['stances']['scorch']['attack_style'] = "magic"

			# Crystal staff is a powered staff
			if 'Crystal staff (' in partial['name']:
				partial['weapon']['weapon_type'] = 'trident-class_weapons'

			## Add useful information to stance
			if partial['weapon'] is not None:
				partial['weapon']['stances'] = {
					k: {**s, 
						'combat_class': get_combat_class(s),
						'weapon_type': partial['weapon']['weapon_type'],
					} for k, s in partial['weapon']['stances'].items()
				}
			
			return partial

		equipment = {}
		for slot in ItemDatabase.SLOTS:
			file_name = f'items-{slot}.json'
			file_path = config.resource_path(Path(f"combat/data/{file_name}"))
			if not file_path.exists() or force_update:
				r = requests.get(SLOT_BASE_URL+'/'+file_name)

				with open(file_path, 'w') as f:
					f.write(r.text)

			with open(file_path, 'r') as f:
				equipment.update({int(ID): filter(item) for ID, item in json.load(f).items() if item['equipable_by_player']})

		# Add an unarmed weapon
		UNARMED_ID = 20720  # Bruma Torch is the same as unarmed
		assert 0 not in equipment
		equipment[0] = deepcopy(equipment[UNARMED_ID])
		equipment[0]['name'] = 'Unarmed'
		equipment[0]['id'] = 0
		equipment[0]['weight'] = 0
		equipment[0]['wiki_url'] = "https://oldschool.runescape.wiki/w/Unarmed"

		return equipment

ITEM_DATABASE = ItemDatabase()

if __name__ == '__main__':
	from pprint import pprint
	import sys
	try:
		pprint(ITEM_DATABASE.find(sys.argv[1]))
	except IndexError:
		print("Incorrect call. Use `python items.py name_of_item` to print item stats.")