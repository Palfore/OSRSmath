""" Notes:
	No damage caps are applied. This damage is the typically attack, so if a weapon can occasionally hit extra damage (verac, keris, etc)
	this is not considered here. Vampyres aren't handled fully, silverlight bonus isn't known, there are likely other exceptions.
	Effects that occur with certain probabilities are not considered here (but will be elsewhere).
	Logic is primarily translated from https://docs.google.com/spreadsheets/d/14ddt-IrH3dmcB7REE1y5AZD51I6dGBfFehQrHp1j1iQ/edit#gid=196557
"""
from math import floor
from osrsmath.combat.items import ITEM_DATABASE
from osrsmath.combat.spells import SPELLBOOK
from pprint import pprint 

class CannotAttackException(ValueError):
	pass

def damage(stance, gear, opponent, effective_levels, prayers, spell=None):
	# Assumes everything is valid, i.e. player.can_attack() == True
	assert not prayers  # Not yet handled
	
	# If casting a spell, or using a magic attack
	if spell is not None or stance['combat_class'] == 'magic':
		return magic_damage(
			spell,
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			effective_levels['magic'],
			sum(i['equipment']['magic_damage'] for i in gear.values()),
		)
	elif stance['combat_class'] == 'melee':
		return melee_damage(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			effective_levels['strength'],
			sum(i['equipment']['melee_strength'] for i in gear.values()),
			prayer_multiplier=1.0
		)
	elif stance['combat_class'] == 'ranged':
		return ranged_damage(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			effective_levels['ranged'],
			sum(i['equipment']['ranged_strength'] for i in gear.values()),
			prayer_multiplier=1.0
		)
	else:
		raise ValueError(f"No combat class could be determined for {stance['combat_style']}.")

def melee_damage(stance, equipment, opponent, effective_strength_level, equipment_strength, prayer_multiplier):
	""" Calculates the maximum hit for a given setup.

	Args:
		stance: dict
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.
	"""
	valid_attack_types = ['slash', 'stab', 'crush']
	valid_attack_styles = ['accurate', 'aggressive', 'controlled', 'defensive']
	if stance['attack_type'] not in valid_attack_types:
		raise CannotAttackException(f'Invalid attack type in given stance: {stance}. Must be one of {valid_attack_types}.')
	if stance['attack_style'] not in valid_attack_styles:
		raise CannotAttackException(f'Invalid attack style in given stance: {stance}. Must be one of {valid_attack_styles}.')

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

	m = m_0
	if opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet', 'Salve amulet (i)']):
		m = floor(m*7/6)
	elif opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (e)', 'Salve amulet (ei)']):
		m = floor(m*1.2)
	elif opponent.has_attribute('slayer_task') and any(e in equipment for e in ['Black mask', 'Black mask (i)', 'Slayer helmet', 'Slayer helmet (i)']):
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
	"""
	valid_attack_types = [None]
	valid_attack_styles = [None]
	if stance['attack_type'] not in valid_attack_types:
		raise CannotAttackException(f'Invalid attack type in given stance: {stance}. Must be one of {valid_attack_types}.')
	if stance['attack_style'] not in valid_attack_styles:
		raise CannotAttackException(f'Invalid attack style in given stance: {stance}. Must be one of {valid_attack_styles}.')

	# Leafy creatures can only be damaged by leaf-bladed equipment.
	if opponent.has_attribute('leafy') and not any(e in equipment for e in ['Broad bolts', 'Broad arrows']):
		return 0

	# Calculate base damage
	# For range - for whatever reason - the attack style is always None.
	# To get the stance bonus, the combat style is either: accurate, short fuse, and flare (although I'm not sure about the last two).
	stance_bonus = {'accurate': 11, 'flare': 11, 'short fuse': 11}.get(stance['combat_style'], 8)
	void_bonus = 1.0
	if 'Void ranger helm' in equipment and 'Void knight gloves' in equipment:
		if 'Void knight top' in equipment and 'Void knight robe' in equipment:
			void_bonus = 1.1
		elif 'Elite void top' in equipment and 'Elite void robe' in equipment:
			void_bonus = 1.125

	m_0 = floor(
		0.5 + (64 + equipment_strength) / 640 * floor(
			floor(
				effective_strength_level * prayer_multiplier + stance_bonus
			) * void_bonus
		)
	)

	m = m_0
	if opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (i)']):
		m = floor(m*7/6)
	elif opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (ei)']):
		m = floor(m*1.2)
	elif opponent.has_attribute('slayer_task') and any(e in equipment for e in ['Black mask (i)', 'Slayer helmet (i)']):
		m = floor(m*1.15)

	if opponent.has_attribute('dragonic') and 'Dragon hunter crossbow' in equipment:
		m = floor(m*1.3)
	elif opponent.has_attribute('wilderness') and "Craw's bow" in equipment:
		m = floor(m*1.5)
	elif "Twisted bow" in equipment:
		cap = 350 if raids else 250
		magic = min(max(opponent.levels['magic'], opponent.equipment['magic_attack']), cap)
		tbow_multipler = (2.5 + int(3*magic - 14) - int(0.3*magic - 140)**2) / 100
		assert 0 <= tbow_multipler <= 2.5
		m = int(m * tbow_multipler)

	if ('Crystal bow' in equipment) and any(f'Crystal {e}' in equipment for e in ['helm', 'body', 'legs']):
		m = floor(m*(1 + 
			(0.003 if "Crystal helm" in equipment else 0) +
			(0.003 if "Crystal body" in equipment else 0) +
			(0.003 if "Crystal legs" in equipment else 0) +
			(0.006 if all(f"Crystal {e}" in equipment for e in ['helm', 'body', 'legs']) else 0)
		))
	return m


def magic_damage(spell, stance, equipment, opponent, effective_strength_level, equipment_strength):
	""" Calculates the maximum hit for a given setup.

	Args:
		stance: dict
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.

	Note:
		A player can wield an powered weapon, but still cast a normal spell (using the book).
	"""
	if spell is None:
		if stance['weapon_type'] != 'trident-class_weapons':
			raise ValueError("Without a spell, only trident-class_weapons can attack with magic.")
			
	# Leafy creatures can only be damaged by leaf-bladed equipment.
	if opponent.has_attribute('leafy') and spell != 'Magic dart':
		return 0
	
	# if SPELLBOOK.requires_undead(spell) and not opponent.has_attribute('undead'):
	# 	raise cant attack. # move this somewhere else
	# if SPELLBOOK.requires_iban(spell) and "Iban's staff" not in equipment:
	# 	raise cant attack # move this somewhere else

	# Calculate base damage	
	if spell is None:  # Powered weapons
		if 'Trident of the seas' in equipment:
			m_0 = int(effective_strength_level / 3 - 5)
		elif 'Trident of the swamp' in equipment:
			m_0 = int(effective_strength_level / 3 - 2)
		elif 'Sanguinesti staff' in equipment:
			m_0 = int(effective_strength_level / 3 - 1)
		elif 'Crystal staff (basic)' in equipment or 'Corrupted staff (basic)' in equipment:
			m_0 = int(effective_strength_level / 3 - 10)
		elif 'Crystal staff (attuned)' in equipment or 'Corrupted staff (attuned)' in equipment:
			m_0 = int(effective_strength_level / 3 - 2)
		elif 'Crystal staff (perfected)' in equipment or 'Corrupted staff (perfected)' in equipment:
			m_0 = int(effective_strength_level / 3 + 6)
		elif 'Black salamander' in equipment:
			m_0 = int(0.5 + effective_strength_level * (64 + 92) / 640)
		elif 'Red salamander' in equipment:
			m_0 = int(0.5 + effective_strength_level * (64 + 77) / 640)
		elif 'Orange salamander' in equipment:
			m_0 = int(0.5 + effective_strength_level * (64 + 59) / 640)
		elif 'Swamp lizard' in equipment:
			m_0 = int(0.5 + effective_strength_level * (64 + 56) / 640)
	else:
		if spell == 'Magic dart':
			if "Slayer's staff (e)" in equipment:
				m_0 = int(13 + effective_strength_level / 6)
			else: 
				m_0 = int(10 + effective_strength_level / 10)
		else:
			m_0 = SPELLBOOK.get(spell)['max_hit']
			if opponent.has_attribute('charge') and SPELLBOOK.can_charge(spell, equipment):
				m_0 += 10

		if 'Chaos gauntlets' in equipment and SPELLBOOK.is_bolt(spell):
			m_0 += 3

	# Calculate multiplier
	multiplier = 1 + equipment_strength / 100
	if any(staff in equipment for staff in ['Mystic smoke staff', 'Smoke battlestaff']) and SPELLBOOK.is_standard(spell):
		multiplier += 0.1
	if "Thammaron's sceptre" in equipment:
		multiplier += 0.25
	if opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (i)']):
		multiplier += 0.15
	elif opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (ei)']):
		multiplier += 0.20
	if 'Void mage helm' in equipment and 'Void knight gloves' in equipment:
		if 'Elite void top' in equipment and 'Elite void robe' in equipment:
			multiplier += 0.025

	# Dawnbringer seems like an exception (?), its calculation is very confusing.
	if 'Dawnbringer' in equipment:
		m = int(int(effective_strength_level * multiplier) / 6 - 1)
	else:
		pre_slayer = m = int(m_0 * multiplier)

	if opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (i)']):
		pass  # Final block executes/applies only if these first two aren't active.
	elif opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (ei)']):
		pass		
	elif opponent.has_attribute('slayer_task') and any(e in equipment for e in ['Black mask (i)', 'Slayer helmet (i)']):
		m = floor(m*1.15)

	if SPELLBOOK.is_fire(spell) and 'Tome of fire' in equipment:
		m = floor(m*1.5)

	if "Eldritch nightmare staff" in equipment:
		m = int(int((44 - int( (99 - min(effective_strength_level, 99)) / 2.27           )) * m) * pre_slayer)
	elif "Volatile staff" in equipment:
		m = int(int((0  - int( (0  - min(effective_strength_level, 99)) * (7/12) + (7/6) )) * m) * pre_slayer)

	return m
