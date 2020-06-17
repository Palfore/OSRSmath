from collections import defaultdict
import fnmatch

def is_only_melee_weapon(weapon):
	# return all(stance['experience'] in ('strength', 'attack', 'defence', 'shared') for stance in weapon['weapon']['stances'])
	# This is too restrictive because of staffs!
	# but looking at 'shared' is worse because all magic and ranged items (pretty much) have shared
	# so instead, since we can't handle shared anyway
	# return weapon['weapon']['weapon_type'] not in ('bow', 'grenade', 'crossbow', 'thrown', 'blaster', 'gun')
	return True

def has_offensive_melee_bonuses(armour):
	return any(amount > 0 for bonus, amount in armour['equipment'].items() if (bonus in [
		"attack_crush", "attack_slash", "attack_stab", "melee_strength",
	])) and armour['equipable_by_player']

def get_offensive_melee_equipment(equipment_data):
	# Reduce the equipment to only those that have a) offensive bonuses, b) melee bonuses
	# Filter for only melee weapons since other attack styles aren't handled yet
	# Also only equipment that gives offensive bonuses, since that is what we're optimizing
	offensive_equipment = defaultdict(list)
	for slot, equipment in equipment_data.items():
		if slot == "weapon" or slot ==  "2h":
			for weapon in equipment.values():
				if is_only_melee_weapon(weapon) and has_offensive_melee_bonuses(weapon):
					offensive_equipment[slot].append(weapon)
		else:
			for armour in equipment.values():
				if has_offensive_melee_bonuses(armour):
					offensive_equipment[slot].append(armour)
	return offensive_equipment

def get_offensive_bonuses(equipment, attack_style=None):
	assert attack_style in ["crush", "slash", "stab", None]
	bonuses = {}
	if equipment['weapon']:
		# Use reciprocal since a greater 1/attack_speed is better,
		# and comparisons are done using >.
		bonuses.update({'reciprocal_attack_speed': 1/equipment['weapon']['attack_speed']})

	if attack_style:
		allowed = [f"attack_{attack_style}", "melee_strength"]
	else:
		allowed = ["attack_crush", "attack_stab", "attack_slash", "melee_strength"]

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

def get_equipable_gear(gear, player_stats, ignore, adjustments):
	equipable = defaultdict(list)
	for i, (slot, slot_equipment) in enumerate(gear.items(), 1):
		for equipment in slot_equipment:
			if any(fnmatch.fnmatch(equipment['name'], i) for i in ignore):  # matches with wildcard support
				 continue

			if equipment['name'] in adjustments:
				equipment['equipment']['requirements'] = adjustments[equipment['name']]

			# If you satisfy a requirement, you can make it None, and choose only from that group
			if equipment['equipment']['requirements']:
				if meets_requirements(player_stats, equipment):
					equipment['equipment']['requirements'] = None
				else:
					continue

			equipable[slot].append(equipment)
	return equipable

class Weapon:
	@staticmethod
	def stance_can_train(stance: dict, skill, allow_controlled=False):
		if stance['experience'] is None:  # Like Dinh's bulwark, on block
			return False
		if allow_controlled and stance['experience'] == 'shared':
			return True # This will probably fail with ranged/magic gear.
		return skill in stance['experience']

	@staticmethod
	def stance_can_use(stance, attack_type):
		assert attack_type in ['stab', 'slash', 'crush', 'ranged', 'magic']
		return stance['attack_type'] == attack_type

	@staticmethod
	def stance_can_do(stance, skill, attack_type, allow_controlled=False):
		return Weapon.stance_can_train(stance, skill, allow_controlled) and \
				Weapon.stance_can_use(stance, attack_type)

	def __init__(self, weapon):
		self.weapon = weapon

	def can_train(self, skill):
		return bool(self.get_skill_stances(skill))

	def get_skill_stances(self, skill, allow_controlled=False):
		return [stance for stance in self.weapon['weapon']['stances']
		           if Weapon.stance_can_train(stance, skill, allow_controlled)]
