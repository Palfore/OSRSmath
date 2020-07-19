from osrsmath.general.player import Player
import osrsmath.combat.boosts as boosts
import osrsmath.combat.damage as damage

def bonus_to_triangle(attack_bonus):
	return {
		'stab': 'melee',
		'slash': 'melee',
		'crush': 'melee',
		'ranged': 'ranged',
		'magic': 'magic',
	}[attack_bonus]

class Fighter(Player):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.stance = None

	def set_stance(self, stance):
		stances = self.equipment.get_stances()
		if stance not in stances:
			raise ValueError(f'''{stance} not a valid stance for the weapon "{self.equipment.gear['weapon']}". Try one of: {list(stances.keys())}.''')
		self.stance = stance

	def get_combat_type(self):
		""" Returns Melee, Ranged, or Magic based on experience gained. """
		stances = self.equipment.get_stances()
		if self.stance is None:
			raise ValueError('The current stance is None, did you forget to set the stance using Fighter.set_stance()?')
		if 'ranged' in stances[self.stance]['experience']:
			return 'Ranged'
		if 'magic' in stances[self.stance]['experience']:
			return 'Magic'
		return bonus_to_triangle(stances[self.stance])['attack_type']


	def get_damage_parameters(self):
		stats = self.equipment.get_stats()
		stances = self.equipment.get_stances()
		if self.get_combat_type() == 'Melee':
			return {
				'offensive_equipment_bonus': stats['melee_strength'],
				'offensive_skill': 'strength',
				'offensive_stance_bonus': {'aggressive': 3, 'controlled': 1}.get(stances[self.stance]['attack_style'], 0),
				'accuracy_equipment_bonus': stats['attack_' + stances[self.stance]['attack_type']],
				'accuracy_skill': 'attack',
				'accuracy_stance_bonus': {'accurate': 3, 'controlled':1}.get(stances[self.stance]['attack_style'], 0),
			}
		elif self.get_combat_type() == 'Ranged':
			return {
				'offensive_equipment_bonus': stats['ranged_strength'],
				'offensive_skill': 'ranged',
				'offensive_stance_bonus': {'accurate': 3}.get(stances[self.stance]['attack_style'], 0),
				'accuracy_equipment_bonus': stats['attack_ranged'],
				'accuracy_skill': 'ranged',
				'accuracy_stance_bonus': {'accurate': 3}.get(stances[self.stance]['attack_style'], 0),
			}
		elif self.get_combat_type() == 'Magic':
			raise ValueError("Magic is not supported")
		else:
			raise ValueError("Could not identify combat type")

	def get_max_hit(self, potion, prayer):
		dmg = self.get_damage_parameters()

		other = boosts.Equipment.none()
		other.update(boosts.other(self.equipment.get_names(), self))
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
		stances = self.equipment.get_stances()

		other = boosts.Equipment.none()
		other.update(boosts.other(self.equipment.get_names(), self))
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

	def get_defence_roll(self):
		assert not using_special, "Special attacks are not implemented"
		stats = self.equipment.get_stats()
		stances = self.equipment.get_stances()

		other = boosts.Equipment.none()
		other.update(boosts.other(self.equipment.get_names()))
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



if __name__ == '__main__':
	from pprint import pprint
	from osrsmath.combat.boosts import Potions, Prayers
	
	fighter = Fighter({'attack': 70, 'strength': 70, 'defence': 70, 'ranged': 70})
	fighter.equipment.wear('Dragon Crossbow')
	fighter.equipment.wear('Runite bolts')
	fighter.set_stance('rapid')
	print(fighter.get_max_hit(Potions.none, Prayers.none))
