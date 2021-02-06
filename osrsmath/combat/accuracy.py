""" Notes:
	This accuracy comes from the typically attack, so if a weapon can occasionally hit with extra accuracy it is not considered here.
	Logic is primarily translated from https://docs.google.com/spreadsheets/d/14ddt-IrH3dmcB7REE1y5AZD51I6dGBfFehQrHp1j1iQ/edit#gid=196557
"""
from math import floor
from osrsmath.combat.items import ITEM_DATABASE
from osrsmath.combat.spells import SPELLBOOK
from pprint import pprint 

class CannotAttackException(ValueError):
	pass

def accuracy(max_attack_roll, max_defence_roll):
	a = max_attack_roll
	d = max_defence_roll
	if a > d:
		return 1 - (d + 2) / (2 * (a + 1))
	else:
		return a / (2 * (d + 1))


def attack_roll(stance, gear, opponent, visible_levels, prayers, spell=None):
	# Assumes everything is valid, i.e. player.can_attack() == True
	assert not prayers  # Not yet handled

	# If casting a spell, or using a magic attack
	if spell is not None or stance['combat_class'] == 'magic':
		return magic_attack_roll(
			spell,
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			visible_levels['magic'],
			sum(i['equipment'][f"attack_magic"] for i in gear.values()),
			prayer_multiplier=1.0
		)	
	elif stance['combat_class'] == 'melee':
		return melee_attack_roll(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			visible_levels['attack'],
			sum(i['equipment'][f"attack_{stance['attack_type']}"] for i in gear.values()),
			prayer_multiplier=1.0
		)
	elif stance['combat_class'] == 'ranged':
		return ranged_attack_roll(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			visible_levels['ranged'],
			sum(i['equipment'][f"attack_ranged"] for i in gear.values()),
			prayer_multiplier=1.0
		)
	else:
		raise ValueError(f"No combat class could be determined for {stance['combat_style']}.")

def melee_attack_roll(stance, equipment, opponent, visible_attack_level, equipment_attack, prayer_multiplier):
	""" Calculates the maximum attack roll for a given setup.

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

	# Calculate base accuracy
	stance_bonus = {'accurate': 11, 'controlled': 9}.get(stance['attack_style'], 8)
	void_bonus = 1.1 if all([
		'Void melee helm' in equipment,
		'Void knight top' in equipment or 'Elite void top' in equipment,
		'Void knight robe' in equipment or 'Elite void robe' in equipment,
		'Void knight gloves' in equipment
	]) else 1.0
	effective_level = floor(void_bonus * (stance_bonus + visible_attack_level))
	a_0 = floor(effective_level * (64 + equipment_attack))

	a = a_0
	
	# Salve and Slayer
	if opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet', 'Salve amulet (i)']):
		a = floor(a*7/6)
	elif opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (e)', 'Salve amulet (ei)']):
		a = floor(a*1.2)
	elif opponent.has_attribute('slayer_task') and any(e in equipment for e in ['Black mask', 'Black mask (i)', 'Slayer helmet', 'Slayer helmet (i)']):
		a = floor(a*7/6)

	# Special Monsters
	if opponent.has_attribute('demon') and 'Arclight' in equipment:
		a = floor(a*1.7)
	elif opponent.has_attribute('dragonic') and 'Dragon hunter lance' in equipment:
		a = floor(a*1.2)
	elif opponent.has_attribute('wilderness') and "Viggora's chainmace" in equipment:
		a = floor(a*1.5)

	# Set Effects
	if all(f'Obsidian {e}' in equipment for e in ['helmet', 'platebody', 'platelegs']) and\
		 any(e in equipment for e in ['Toktz-xil-ek', 'Toktz-xil-ak', 'Tzhaar-ket-em', 'Tzhaar-ket-om', 'Tzhaar-ket-om (t)']):
		a = floor(a*1.1)
	elif stance['attack_type'] == 'crush':
		a = floor(a*(1 + 
			(0.005 if "Inquisitor's great helm" in equipment else 0) +
			(0.005 if "Inquisitor's hauberk"    in equipment else 0) +
			(0.005 if "Inquisitor's plateskirt" in equipment else 0) +
			(0.010 if all(f"Inquisitor's {e}" in equipment for e in ["great helm", "hauberk", "plateskirt"]) else 0)
		))

	if 'Berserker necklace' in equipment and any(e in equipment for e in ['Toktz-xil-ek', 'Toktz-xil-ak', 'Tzhaar-ket-em', 'Tzhaar-ket-om', 'Tzhaar-ket-om (t)']):
		a = floor(a*1.2)

	return a


def ranged_attack_roll(stance, equipment, opponent, visible_attack_level, equipment_attack, prayer_multiplier):
	""" Calculates the maximum attack roll for a given setup.

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
	if opponent.has_attribute('leafy') and not any(f'Leaf-bladed {e}' in equipment for e in ['battleaxe', 'spear', 'sword']):
		return 0

	# Calculate base accuracy
	# For range - for whatever reason - the attack style is always None.
	# To get the stance bonus, the combat style is either: accurate, short fuse, and flare (although I'm not sure about the last two).
	stance_bonus = {'accurate': 11, 'flare': 11, 'short fuse': 11}.get(stance['combat_style'], 8)
	void_bonus = 1.1 if all([
		'Void ranger helm' in equipment,
		'Void knight top' in equipment or 'Elite void top' in equipment,
		'Void knight robe' in equipment or 'Elite void robe' in equipment,
		'Void knight gloves' in equipment
	]) else 1.0
	effective_level = floor(void_bonus * (stance_bonus + visible_attack_level))
	a_0 = floor(effective_level * (64 + equipment_attack))
	
	a = a_0
	# Salve and Slayer. Salve only gives ranged accuracy if imbued (i).
	if opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (i)']):
		a = floor(a*7/6)
	elif opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (ei)']):
		a = floor(a*1.2)
	elif opponent.has_attribute('slayer_task') and any(e in equipment for e in ['Black mask (i)', 'Slayer helmet (i)']):
		a = floor(a*1.15)

	# Special Monsters
	if opponent.has_attribute('dragonic') and 'Dragon hunter crossbow' in equipment:
		a = floor(a*1.3)
	elif opponent.has_attribute('wilderness') and "Craw's bow" in equipment:
		a = floor(a*1.5)
	elif "Twisted bow" in equipment:
		cap = 350 if raids else 250
		magic = min(max(opponent.levels['magic'], opponent.equipment['magic_attack']), cap)
		tbow_multipler = (1.4 + int(3*magic - 10) - int(0.3*magic - 100)**2) / 100
		assert 0 <= tbow_multipler <= 1.4
		a = int(a * tbow_multipler)

	# Set Effects
	if ('Crystal bow' in equipment) and any(f'Crystal {e}' in equipment for e in ['helm', 'body', 'legs']):
		a = floor(a*(1 + 
			(0.006 if "Crystal helm" in equipment else 0) +
			(0.006 if "Crystal body" in equipment else 0) +
			(0.006 if "Crystal legs" in equipment else 0) +
			(0.0012 if all(f"Crystal {e}" in equipment for e in ['helm', 'body', 'legs']) else 0)
		))
	
	return a


def magic_attack_roll(spell, stance, equipment, opponent, visible_magic_level, equipment_attack, prayer_multiplier):
	""" Calculates the maximum hit for a given setup.

	Args:
		stance: dict
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.

	Note:
		A player can wield an powered weapon (or any weapon), but still cast a normal spell (using the book).
		This means that the spell being None or a valid spell is what determines the calculation.
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

	# Calculate base accuracy
	# For magic - for whatever reason - the attack style is always None.
	# To get the stance bonus, the combat style is either: accurate, or longrange for powered staves.
	if spell is None:  # Only bonuses for powered staves
		stance_bonus = {'accurate': 11, 'longrange': 9}.get(stance['combat_style'], 8)
	else:
		stance_bonus = 8

	void_bonus = 1.45 if all([
		'Void mage helm' in equipment,
		'Void knight top' in equipment or 'Elite void top' in equipment,
		'Void knight robe' in equipment or 'Elite void robe' in equipment,
		'Void knight gloves' in equipment
	]) else 1.0
	effective_level = floor(void_bonus * (stance_bonus + visible_magic_level))
	a_0 = floor(effective_level * (64 + equipment_attack))
	a = a_0

	# Calculate base accuracy	
	if spell is None:  # Powered weapons
		pass
	else:
		if 'Mystic smoke staff' in equipment:
			a *= int(a*1.1)
	
	# Salve and Slayer. Salve only gives ranged accuracy if imbued (i).
	if opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (i)']):
		a = floor(a*1.15)
	elif opponent.has_attribute('undead') and any(e in equipment for e in ['Salve amulet (ei)']):
		a = floor(a*1.2)
	elif opponent.has_attribute('slayer_task') and any(e in equipment for e in ['Black mask (i)', 'Slayer helmet (i)']):
		a = floor(a*1.15)
	
	return a




if __name__ == '__main__':
	from osrsmath.combat.items import ITEM_DATABASE
	from pprint import pprint
	from osrsmath.combat.fighter import Fighter
	dscim = ITEM_DATABASE.find('Dragon scimitar')
	cbow = ITEM_DATABASE.find('Crystal bow')
	# astaff = ITEM_DATABASE.find('Air battlestaff')
	staff = ITEM_DATABASE.find('Trident of the swamp')

	# a = attack_roll(
	# 	dscim['weapon']['stances']['chop'],
	# 	{'weapon': dscim},
	# 	Fighter(100, {}, []), 
	# 	{'attack': 90},
	# 	prayers=[],
	# 	spell=None,
	# )

	# a = attack_roll(
	# 	cbow['weapon']['stances']['accurate'],
	# 	{'weapon': cbow},
	# 	Fighter(100, {}, []), 
	# 	{'ranged': 90},
	# 	prayers=[],
	# 	spell=None,
	# )

	for i in ['Starter staff', 'Trident of the seas', 'Sanguinesti staff', 'Dawnbringer', 'Trident of the swamp', 'Crystal staff (attuned)']:
		pprint(ITEM_DATABASE.find(i))
	# pprint(staff)
	a = attack_roll(
		# ITEM_DATABASE.find('Unarmed')['weapon']['stances']['punch'],
		staff['weapon']['stances']['accurate'],
		{'weapon': staff},
		Fighter(100, {}, []), 
		{'magic': 78, 'attack': 50},
		prayers=[],
		# spell='Air bolt',
	)


	print(a)

	