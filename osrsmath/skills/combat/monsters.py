from pprint import pprint, pformat
from pathlib import Path
import requests
import json
import os

import osrsmath.config as config
import osrsmath.skills.combat.damage as damage
from osrsmath.general.constants import TICK_DURATION
import osrsmath.skills.combat.distributions as distributions
import osrsmath.skills.combat.accuracy as accuracy


MONSTER_LIST_BASE_URL = "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/docs"


class Monster:
	ALLOWED_ATTRIBUTES = ['kalphite', 'shade', 'dragonic', 'leafy', 'wilderness', 'demon', 
	                      'undead', 'slayer_task', 'vampyre', 'charge', 'npc']
	
	def __init__(self, data):
		self.id = data['id']
		self.name = data['name']
		self.members = data['members']
		self.size = data['size']

		self.attributes = data['attributes'] + ['npc']
		self.attack_types = data['attack_type']
		if self.name == 'Abyssal demon':
			pprint(data['max_hit'])
		self.hitpoints = data['hitpoints']
		self._max_hit = data['max_hit']
		self._attack_speed = data['attack_speed']
		self.combat_level = data['combat_level']
		self.levels = {
			t: data[f'{t}_level'] for t in ['attack', 'strength', 'defence', 'magic', 'ranged']
		}
		self.bonuses = {
			t: data[t] for t in ['attack_crush', 'attack_stab', 'attack_magic', 'attack_ranged', 'attack_slash', 'defence_crush', 'defence_magic', 'defence_ranged', 'defence_slash', 'defence_stab', 'magic_damage', 'melee_strength', 'ranged_strength']
		}

		self.poison = {
			t: data[t] for t in ['immune_poison', 'immune_venom', 'poisonous']
		}
		self.slayer = {
			t: data[f'slayer_{t}'] for t in ['level', 'masters', 'monster', 'xp',]
		}
		self.wiki = {
			t: data[f'wiki_{t}'] for t in ['name', 'url']
		}
		self.spell = None

	def has_attribute(self, attribute: str):
		if attribute not in self.ALLOWED_ATTRIBUTES:
			raise ValueError(f'The requested attribute, "{attribute}", must be one of: {self.ALLOWED_ATTRIBUTES}.')
		if self.attributes:
			return attribute in self.attributes
		return False

	def max_hit(self, opponent):
		return self._max_hit

	def attack_speed(self):
		return self._attack_speed

	def attack_interval(self):
		return self.attack_speed() * TICK_DURATION
	
	def accuracy(self, opponent):
		return accuracy.accuracy(self.attack_roll(opponent), opponent.defence_roll(self))

	def attack_roll(self, opponent):
		if len(self.attack_types) == 0:
			raise NotImplementedError(f"Not sure how to handle no attack types for {self.name}.")
		elif len(self.attack_types) > 1:
			raise NotImplementedError(f"Multiple attacks not yet supported for {self.name}.")
		
		at = self.attack_types[0]
		if at == 'dragonfire':
			raise NotImplementedError(f"Dragonfire not yet supported for {self.name}.")
		elif at == 'typeless':
			raise NotImplementedError(f"Typeless attacks not yet supported for {self.name}.")
		elif at == 'melee':
			raise NotImplementedError(f"Not sure how to handle 'melee' attack style for {self.name}.")
		elif at in ['stab', 'crush', 'slash']:
			attack_level = self.levels['attack']
		elif at in ['ranged', 'magic']:
			attack_level = self.levels[at]
		else:
			raise ValueError(f"Couldn't parse attack type for {self.name}")
		
		equipment_attack = self.bonuses[f"attack_{opponent.stance['attack_type']}"]
		
		A = int( (9 + attack_level) * (64 + equipment_attack) )
		return A

	def defence_roll(self, opponent):
		defence_level = self.levels['defence']
		equipment_defence = self.bonuses[f"defence_{opponent.stance['attack_type']}"]
		D = int( (9 + defence_level) * (64 + equipment_defence) )
		return D

	def damage_distribution(self, opponent):
		def distribution_as_dict():
			return distributions.standard(self.max_hit(opponent), self.accuracy(opponent))
		return distributions.DamageDistribution(distribution_as_dict())

	def __repr__(self):
		return pformat(self.__dict__)

class MonsterDatabase:
	def __init__(self):
		self.monsters = MonsterDatabase.get_monsters()
		self.IDs = {monster.name: ID for ID, monster in self.monsters.items()}

	def find(self, name: str):
		if name not in self.IDs:
			raise KeyError(f'Could not find item named "{name}" in the item database.')
		return self.get(self.IDs[name])
		
	def get(self, ID: int):
		if ID not in self.monsters:
			raise KeyError(f'Could not find item with id {ID} in the item database.')
		return self.monsters[ID]

	@staticmethod
	def get_monsters(force_update=False):
		def filter(i):
			return Monster(i)

		file_name = 'monsters-complete.json'
		file_path = config.resource_path(Path(f"skills/combat/data/{file_name}"))
		if not file_path.exists() or force_update:
			r = requests.get(MONSTER_LIST_BASE_URL+'/'+file_name)
			if r.status_code != 200:
				raise ValueError("Unable to retrieve monster data.")
			with open(file_path, 'w') as f:
				f.write(r.text)

		with open(file_path, 'r') as f:
			monsters = {int(ID): filter(item) for ID, item in json.load(f).items()}

		return monsters

MONSTER_DATABASE = MonsterDatabase()

if __name__ == '__main__':
	from pprint import pprint as pp
	from osrsmath.combat.fighter import Fighter, Duel
	attacker = Fighter(99, {	
			'attack': 90,
			'strength': 90,
			'defence': 54,
			'magic': 80,
			'ranged': 90,
		}, [
			'Rune kiteshield',
			'Dragon scimitar',
		]
	)
	attacker.set_stance('slash')
	defender = MONSTER_DATABASE.find('Abyssal demon')
	
	pprint(Duel(attacker, defender).summary())















