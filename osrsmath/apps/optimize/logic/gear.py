from osrsmath.combat.equipment import EquipmentPool
from osrsmath.combat.fighter import bonus_to_triangle
from collections import defaultdict
import fnmatch

def has_offensive_bonuses(armour, triangle):
	def bool_from_stats(stats):
		return any(
			amount > 0 for bonus, amount in armour['equipment'].items() if bonus in stats
		) and armour['equipable_by_player']

	if triangle.lower() == 'melee':
		return bool_from_stats(["attack_crush", "attack_slash", "attack_stab", "melee_strength"])
	elif triangle.lower() == 'ranged':
		return bool_from_stats(["attack_ranged", "ranged_strength"])
	elif triangle.lower() == 'magic':
		return bool_from_stats(["attack_magic", "magic_damage"])

def get_offensive_equipment(triangle):
	# Reduce the equipment to only those that have a) offensive bonuses, b) melee bonuses
	# Filter for only melee weapons since other attack styles aren't handled yet
	# Also only equipment that gives offensive bonuses, since that is what we're optimizing
	offensive_equipment = defaultdict(list)
	for slot, equipment in EquipmentPool().equipment.items():
		if slot == "weapon" or slot ==  "2h":
			for weapon in equipment.values():
				if has_offensive_bonuses(weapon, triangle):
					offensive_equipment[slot].append(weapon)
		else:
			for armour in equipment.values():
				if has_offensive_bonuses(armour, triangle):
					offensive_equipment[slot].append(armour)
	return offensive_equipment

def get_offensive_bonuses(equipment, attack_style):
	bonuses = {}
	if equipment['weapon']:
		# Use reciprocal since a greater 1/attack_speed is better,
		# and comparisons are done using >.
		bonuses.update({'reciprocal_attack_speed': 1/equipment['weapon']['attack_speed']})

	allowed = [f"attack_{attack_style}", {
			'melee': "melee_strength",
			'ranged': "ranged_strength",
			'magic': "magic_damage",
		}[bonus_to_triangle(attack_style)]
	]
	bonuses.update({stat:value for stat, value in equipment['equipment'].items() if stat in allowed})
	return bonuses

def meets_requirements(player_stats, equipment):
	if equipment['equipment']['requirements'] is None:
		return True
	for stat, req in equipment['equipment']['requirements'].items():
		if stat not in player_stats:
			raise ValueError(f"Supply your {stat} level to check {equipment['name']} for: {equipment['equipment']['requirements']}")
		if player_stats[stat] < req:
			return False
	return True

def get_equipable_gear(training_skill, gear, player_stats, ignore, adjustments):
	equipable = defaultdict(list)
	for slot, slot_equipment in gear.items():
		for equipment in slot_equipment:
			if any(fnmatch.fnmatch(equipment['name'], item) for item in ignore):  # matches with wildcard support
				 continue

			if equipment['name'] in adjustments:
				equipment['equipment']['requirements'] = adjustments[equipment['name']]

			# If you satisfy a requirement, you can make it None, and choose only from that group
			if equipment['equipment']['requirements']:
				if meets_requirements(player_stats, equipment):
					equipment['equipment']['requirements'] = None
				else:
					continue

			# You must be able to train the desired skill, if you are a weapon
			if slot == '2h' or slot == 'weapon':
				if not any(Weapon.stance_can_train(stance, training_skill) \
						for stance in equipment['weapon']['stances']):
					continue
			equipable[slot].append(equipment)
	return equipable

class Weapon:
	@staticmethod
	def stance_can_train(stance: dict, skill):
		if stance['experience'] is None:  # Like Dinh's bulwark, on block
			return False

		if stance['experience'] == 'shared':  # Melee
			return skill == 'controlled'
		return skill == stance['experience']

	@staticmethod
	def stance_can_use(stance, attack_type):
		assert attack_type in ['stab', 'slash', 'crush', 'ranged', 'magic']
		if stance['attack_type'] is None:
			if stance['experience'] is None:  # Dinh's bulwark
				return False
			return attack_type in stance['experience']  # Ranged
		if stance['attack_type'] in ('defensive casting', 'spellcasting'):
			return True
		else:
			return stance['attack_type'] == attack_type
			

	@staticmethod
	def stance_can_do(stance, skill, attack_type):
		train = Weapon.stance_can_train(stance, skill)
		use = Weapon.stance_can_use(stance, attack_type)
		return train and use

	def __init__(self, weapon):
		self.weapon = weapon

	def can_train(self, skill):
		return bool(self.get_skill_stances(skill))

	def get_skill_stances(self, skill):
		return [stance for stance in self.weapon['weapon']['stances']
		           if Weapon.stance_can_train(stance, skill)]
