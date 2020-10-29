from math import floor
from osrsmath.combat.items import ITEM_DATABASE
from pprint import pprint 

class CannotAttackException(ValueError):
	pass


def melee_damage(stance, equipment, opponent, effective_strength_level, equipment_strength, prayer_multiplier):
	""" Calculates the maximum hit for a given setup.

	Args:
		stance: dict
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.
	Notes:
		No damage caps are applied. This damage is the typically attack, so if a weapon can occasionally hit extra damage (verac, keris, etc)
		this is not considered here. Vampyres aren't handled fully, silverlight bonus isn't known, there are likely other exceptions.

	"""
	# Exceptions
	salamanders = {
		'Black salamander': 'Harralander tar', 'Red salamander': 'Tarromin tar',
		'Orange salamander': 'Marrentill tar', 'Swamp lizard': 'Guam tar'
	}
	for salamander, tar in salamanders.items():
		if salamander in equipment:
			if tar not in equipment:
				raise CannotAttackException(f'{salamander} require {tar} as ammunition for all attack styles.')

			if stance['combat_style'] == 'scorch':
				stance['attack_style'] = 'aggressive'  # The database attack style is None, but should be aggressive for melee.
			else:
				# The player may be able to attack, but this is an invalid way to call this code since it's not melee.
				raise ValueError(f'Salamanders can only deal melee damage using the Scorch combat style, not {stance["combat_style"]}.')

	if stance['attack_type'] not in ['slash', 'stab', 'crush']:
		raise CannotAttackException(f'Invalid attack type in given stance: {stance}. Must be one of [slash, stab, crush].')
	if stance['attack_style'] not in ['accurate', 'aggressive', 'controlled', 'defensive']:
		raise CannotAttackException(f'Invalid attack style in given stance: {stance}. Must be one of [accurate, aggressive, controlled, defensive].')

	# Leafy creatures can only be damaged by leaf-bladed equipment.
	if opponent.has_attribute('leafy') and not any(f'Leaf-bladed {e}' in equipment for e in ['battleaxe', 'spear', 'sword']):
		return 0

	# Calculate base damage
	stance_bonus = {'aggressive': 11, 'controlled': 9}.get(stance['attack_style'], 8)
	void_bonus = 1.1 if all([
		'Void melee helm' in equipment,
		'Void knight top' in equipment or 'Elite void top' in equipment,
		'Void knight robe' in equipment or 'Elite void robe' in equipment,
		'Void knight gloves' in equipment
	]) else 1.0
	m_0 = floor(
		0.5 + (64 + equipment_strength) / 640 * floor(
			floor(
				effective_strength_level * prayer_multiplier + stance_bonus
			) * void_bonus
		)
	)

	# This logic is primarily translated from https://docs.google.com/spreadsheets/d/14ddt-IrH3dmcB7REE1y5AZD51I6dGBfFehQrHp1j1iQ/edit#gid=196557
	m = m_0
	if opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet', 'Salve amulet (i)']):
		m = floor(m*7/6)
	elif opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (e)', 'Salve amulet (ei)']):
		m = floor(m*1.2)
	elif opponent.has_attribute('slayer_task') and any(e in equipment for e in ['Black mask', 'Slayer helmet', 'Slayer helmet (i)']):
		m = floor(m*7/6)

	if opponent.has_attribute('demon') and 'Arclight' in equipment:
		m = floor(m*1.7)
	elif opponent.has_attribute('leafy') and 'Leaf-bladed battleaxe' in equipment:
		m = floor(m*1.175)
	elif opponent.has_attribute('dragonic') and 'Dragon hunter lance' in equipment:
		m = floor(m*1.2)
	elif opponent.has_attribute('wilderness') and "Viggora's chainmace" in equipment:
		m = floor(m*1.5)

	if all(f'Obsidian {e}' in equipment for e in ['helmet', 'platebody', 'platelegs']) and\
		 any(e in equipment for e in ['Toktz-xil-ek', 'Toktz-xil-ak', 'Tzhaar-ket-em', 'Tzhaar-ket-om', 'Tzhaar-ket-om (t)']):
		m = floor(m*1.1)
	elif stance['attack_type'] == 'crush':
		m = floor(m*(1 + 
			(0.005 if "Inquisitor's great helm" in equipment else 0) +
			(0.005 if "Inquisitor's hauberk"    in equipment else 0) +
			(0.005 if "Inquisitor's plateskirt" in equipment else 0) +
			(0.010 if all(f"Inquisitor's {e}" in equipment for e in ["great helm", "hauberk", "plateskirt"]) else 0)
		))

	if 'Berserker necklace' in equipment and any(e in equipment for e in ['Toktz-xil-ek', 'Toktz-xil-ak', 'Tzhaar-ket-em', 'Tzhaar-ket-om', 'Tzhaar-ket-om (t)']):
		m = floor(m*1.2)

	if (opponent.has_attribute('demon') or opponent.has_attribute('vampyre')) and 'Darklight' in equipment:
		m = floor(m*1.6)
	elif all(f"Dharok's {e}" in equipment for e in ['helm', 'platebody', 'platelegs', 'greataxe']):
		m = floor(m*(
			1 + (player.hitpoints - player.levels['hitpoints'])/100*player.hitpoints/100  # Seems weird
		))
	elif opponent.has_attribute('shade') and 'Gadderhammer' in equipment:
		m = floor(m*1.25)
	elif opponent.has_attribute('kalphite') and 'Keris' in equipment:
		m = floor(m*4/3)

	return m

def ranged_damage(stance, equipment, opponent, effective_strength_level, equipment_strength, prayer_multiplier):
	""" Calculates the maximum hit for a given setup.

	Args:
		stance: dict
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.
	Notes:
		No damage caps are applied. This damage is the typically attack, so if a weapon can occasionally hit extra damage (verac, keris, etc)
		this is not considered here. Vampyres aren't handled fully, silverlight bonus isn't known, there are likely other exceptions.

	"""
	# Exceptions
	salamanders = {
		'Black salamander': 'Harralander tar', 'Red salamander': 'Tarromin tar',
		'Orange salamander': 'Marrentill tar', 'Swamp lizard': 'Guam tar'
	}
	for salamander, tar in salamanders.items():
		if salamander in equipment:
			if tar not in equipment:
				raise CannotAttackException(f'{salamander} require {tar} as ammunition for all attack styles.')

			if stance['combat_style'] == 'Flare':
				print(stance['attack_style'])
				# stance['attack_style'] = 'aggressive'  # The database attack style is None, but should be aggressive for melee.
			else:
				# The player may be able to attack, but this is an invalid way to call this code since it's not ranged.
				raise ValueError(f'Salamanders can only deal ranged damage using the Flare combat style, not {stance["combat_style"]}.')

	valid_attack_types = [None]
	valid_attack_styles = [None]
	if stance['attack_type'] not in valid_attack_types:
		raise CannotAttackException(f'Invalid attack type in given stance: {stance}. Must be one of {valid_attack_types}.')
		# raise CannotAttackException(f'Invalid attack type in given stance: {stance}. Must be one of [ranged].')
	if stance['attack_style'] not in valid_attack_styles:
		raise CannotAttackException(f'Invalid attack style in given stance: {stance}. Must be one of {valid_attack_styles}.')

	# Leafy creatures can only be damaged by leaf-bladed equipment.
	# if opponent.has_attribute('leafy') and not any(f'Leaf-bladed {e}' in equipment for e in ['battleaxe', 'spear', 'sword']):
	# 	return 0

	# Calculate base damage
	stance_bonus = {'aggressive': 11, 'controlled': 9}.get(stance['attack_style'], 8)
	void_bonus = 1.1 if all([
		'Void ranger helm' in equipment,
		'Void knight top' in equipment or 'Elite void top' in equipment,
		'Void knight robe' in equipment or 'Elite void robe' in equipment,
		'Void knight gloves' in equipment
	]) else 1.0
	m_0 = floor(
		0.5 + (64 + equipment_strength) / 640 * floor(
			floor(
				effective_strength_level * prayer_multiplier + stance_bonus
			) * void_bonus
		)
	)

	# This logic is primarily translated from https://docs.google.com/spreadsheets/d/14ddt-IrH3dmcB7REE1y5AZD51I6dGBfFehQrHp1j1iQ/edit#gid=196557
	m = m_0
	return m

def damage(stance, gear, opponent, effective_levels, prayers):
	assert prayers is None
	
	if stance['combat_class'] == 'melee':
		return -1
		return melee_damage(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			effective_levels['strength'],
			sum(i['equipment']['melee_strength'] for i in gear.values()),
			prayer_multiplier=1.0
		)
	elif stance['combat_class'] == 'ranged':
		weapon_type = gear['weapon']['weapon']['weapon_type']
		if weapon_type == 'bows':
			if any(gear['weapon']['name'].endswith(suffix) for suffix in ['shortbow', 'longbow']):
				print('Need arrows')


		return ranged_damage(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			effective_levels['strength'],
			sum(i['equipment']['melee_strength'] for i in gear.values()),
			prayer_multiplier=1.0
		)
	elif stance['combat_class'] == 'magic':
		return -1
		pass
	else:
		raise CannotAttackException(f"No combat class could be determined for {stance['combat_style']}.")
