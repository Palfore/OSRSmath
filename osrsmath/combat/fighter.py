from osrsmath.general.player import Player
import osrsmath.combat.boosts as boosts
import osrsmath.combat.damage as damage

from typing import Optional

def bonus_to_triangle(attack_bonus: str):
	""" Converts the attack bonus to the corresponding combat triangle. 

	See source for more details.

	Args:
		attack_bonus: One of stab, slash, crush, ranged, magic.
			or "defensive casting"

	Returns:
		One of melee, ranged, magic.
	"""
	return {
		'stab': 'melee',
		'slash': 'melee',
		'crush': 'melee',
		'ranged': 'ranged',
		'magic': 'magic',
	}[attack_bonus]

def stance_to_style(combat_type: str, stance: dict):
	""" Returns the equipment bonus name of the current stance. 
	
	Returns:
		One of stab, slash, crush, magic, ranged
	"""
	if combat_type in ('ranged', 'magic'):
		return combat_type
	return stance['attack_type']


class Fighter(Player):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.stance = None
		self.spell = None

	def set_stance(self, stance: str):
		""" Sets the attack stance.
		
		Raises:
			ValueError If `stance` is not part of `Fighter(..).equipment.get_stances()`.
		"""
		stances = self.equipment.get_stances()
		if stance not in stances:
			raise ValueError(f'''{stance} not a valid stance for the weapon "{self.equipment.gear['weapon']}". Try one of: {list(stances.keys())}.''')
		self.stance = stance

	def set_spell(self, spell: Optional[str]=None):
		""" Sets the attack spell.

		None will clear the spell.
		"""
		self.spell = spell

	def get_combat_type(self):
		""" Returns Melee, Ranged, or Magic based on experience gained.
	
		Raises:
			ValueError if the current stance is not set. See `Fighter.set_stance`.

		Returns:
			One of melee, ranged, magic
		"""
		stances = self.equipment.get_stances()
		if self.stance is None:
			raise ValueError('The current stance is None, did you forget to set the stance using Fighter.set_stance()?')
		if 'ranged' in stances[self.stance]['experience']:
			return 'ranged'
		if 'magic' in stances[self.stance]['experience']:
			return 'magic'
		return bonus_to_triangle(stances[self.stance]['attack_type'])

	def get_attack_style(self):
		""" Returns the equipment bonus name of the current stance. 
		
		Returns:
			One of stab, slash, crush, magic, ranged
		"""
		return stance_to_style(self.get_combat_type(), self.equipment.get_stances()[self.stance])

	def get_damage_parameters(self):
		self.get_attack_style()
		stats = self.equipment.get_stats()
		stances = self.equipment.get_stances()
		if self.get_combat_type() == 'melee':
			return {
				'offensive_equipment_bonus': stats['melee_strength'],
				'offensive_skill': 'strength',
				'offensive_stance_bonus': {'aggressive': 3, 'controlled': 1}.get(stances[self.stance]['attack_style'], 0),
				'accuracy_equipment_bonus': stats['attack_' + stances[self.stance]['attack_type']],
				'accuracy_skill': 'attack',
				'accuracy_stance_bonus': {'accurate': 3, 'controlled':1}.get(stances[self.stance]['attack_style'], 0),
			}
		elif self.get_combat_type() == 'ranged':
			return {
				'offensive_equipment_bonus': stats['ranged_strength'],
				'offensive_skill': 'ranged',
				'offensive_stance_bonus': {'accurate': 3}.get(stances[self.stance]['attack_style'], 0),
				'accuracy_equipment_bonus': stats['attack_ranged'],
				'accuracy_skill': 'ranged',
				'accuracy_stance_bonus': {'accurate': 3}.get(stances[self.stance]['attack_style'], 0),
			}
		elif self.get_combat_type() == 'magic':
			return {
				'offensive_equipment_bonus': stats['magic_damage'],
				'offensive_skill': 'magic',
				'offensive_stance_bonus': 0,
				'accuracy_equipment_bonus': stats['attack_magic'],
				'accuracy_skill': 'magic',
				'accuracy_stance_bonus': 0,
			}
		else:
			raise ValueError("Could not identify combat type")

	def get_attack_speed(self):
		boost = self.equipment.get_stances()[self.stance]['boosts']
		attack_speed = self.equipment.get_stats()['attack_speed']
		if boost == 'attack speed by 1 tick':
			attack_speed -= 0.6
		return attack_speed

	def get_max_hit(self, potion, prayer):
		dmg = self.get_damage_parameters()

		other = boosts.Equipment.none()
		other.update(boosts.other(self.equipment.get_names(), self))
		special_attack_bonus = 1  # Special attacks are not implemented
		multipler = 1  # Ignoring flooring order, since there is no official documentation
		
		if self.get_combat_type() == 'magic':
			if self.spell is None:
				raise ValueError("The fighter's spell is None, consider using `Fighter.set_spell`.")
			return damage.Magic().max_hit(
				self.spell,
				dmg['offensive_equipment_bonus'],
				self.levels[dmg['offensive_skill']],
				potion(self.levels[dmg['offensive_skill']]),
				prayer(dmg['offensive_skill']),
				other[dmg['offensive_skill']],
				# dmg['offensive_stance_bonus'],
				special_attack_bonus, multipler
			)

		if self.spell is not None:
			raise ValueError(f"The fighter's spell is '{self.spell}', for {self.get_combat_type()} use `Fighter.set_spell(None)`.")
		return damage.Standard().max_hit(
			dmg['offensive_equipment_bonus'],
			self.levels[dmg['offensive_skill']],
			potion(self.levels[dmg['offensive_skill']]),
			prayer(dmg['offensive_skill']),
			other[dmg['offensive_skill']],
			dmg['offensive_stance_bonus'],
			special_attack_bonus, multipler
		)

	def get_attack_roll(self, potion, prayer):
		dmg = self.get_damage_parameters()
		stances = self.equipment.get_stances()

		other = boosts.Equipment.none()
		other.update(boosts.other(self.equipment.get_names(), self))
		multipler = 1  # Ignoring flooring order, since there is no official documentation

		if self.get_combat_type() == 'magic':
			return damage.Magic().max_attack_roll(
				dmg['accuracy_equipment_bonus'],
				self.levels[dmg['accuracy_skill']],
				potion(self.levels[dmg['accuracy_skill']]),
				prayer(dmg['accuracy_skill']),
				other[dmg['accuracy_skill']],
				dmg['accuracy_stance_bonus'],
				multipler
			)
		return damage.Standard().max_attack_roll(
			dmg['accuracy_equipment_bonus'],
			self.levels[dmg['accuracy_skill']],
			potion(self.levels[dmg['accuracy_skill']]),
			prayer(dmg['accuracy_skill']),
			other[dmg['accuracy_skill']],
			dmg['accuracy_stance_bonus'],
			multipler
		)

	def get_defence_roll(self):
		assert not using_special, "Special attacks are not implemented"
		stats = self.equipment.get_stats()
		stances = self.equipment.get_stances()

		other = boosts.Equipment.none()
		other.update(boosts.other(self.equipment.get_names()))
		multipler = 1  # Ignoring flooring order, since there is no official documentation
		if self.get_combat_type() in ('melee', 'ranged'):
			return damage.Standard().max_defence_roll(
				stats['defence_' + attacker_attack_type],
				self.levels['defence'],
				potion(self.levels['defence']),
				prayer('defence'),
				other['defence'],
				{'longrange': 3, 'defensive': 3, 'controlled': 1,}.get(stances[self.combat_style]['attack_style'], 0),
				multipler
			)
		elif self.get_combat_type() == 'magic':
			raise ValueError("Magic defence roll is not supported")
		else:
			raise ValueError("Could not identify combat type")



if __name__ == '__main__':
	from pprint import pprint
	from osrsmath.combat.boosts import Potions, Prayers
	
	fighter = Fighter({'attack': 70, 'strength': 70, 'defence': 70, 'ranged': 70})
	fighter.equipment.wear('Dragon Crossbow')
	fighter.equipment.wear('Runite bolts')
	fighter.set_stance('rapid')
	print(fighter.get_max_hit(Potions.none, Prayers.none))
