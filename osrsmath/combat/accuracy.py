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


def attack_roll(stance, gear, opponent, visible_levels, prayers, spell):
	# Assumes everything is valid, i.e. player.can_attack() == True
	assert not prayers  # Not yet handled
	if stance['combat_class'] == 'melee':
		if spell is not None:
			raise ValueError(f'The spell is set to "{spell}", but should be None.')
		return melee_attack_roll(
			stance,
			[i['name'] for i in gear.values()],
			opponent,
			visible_levels['attack'],
			sum(i['equipment'][f"attack_{stance['attack_type']}"] for i in gear.values()),
			prayer_multiplier=1.0
		)
	else:
		raise CannotAttackException(f"No combat class could be determined for {stance['combat_style']}.")

def melee_attack_roll(stance, equipment, opponent, visible_attack_level, equipment_attack, prayer_multiplier):
	""" Calculates the maximum attack roll for a given setup.

	Args:
		stance: dict
			stance['attack_type'] must be a valid attack type.
			stance['attack_style'] must be a valid attack style.
	"""
	if stance['attack_type'] not in ['slash', 'stab', 'crush']:
		raise CannotAttackException(f'Invalid attack type in given stance: {stance}. Must be one of [slash, stab, crush].')
	if stance['attack_style'] not in ['accurate', 'aggressive', 'controlled', 'defensive']:
		raise CannotAttackException(f'Invalid attack style in given stance: {stance}. Must be one of [accurate, aggressive, controlled, defensive].')

	# Leafy creatures can only be damaged by leaf-bladed equipment.
	if opponent.has_attribute('leafy') and not any(f'Leaf-bladed {e}' in equipment for e in ['battleaxe', 'spear', 'sword']):
		return 0

	# Calculate base damage
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



if __name__ == '__main__':
	from osrsmath.combat.items import ITEM_DATABASE
	from pprint import pprint
	from osrsmath.combat.fighter import Fighter
	dscim = ITEM_DATABASE.find('Dragon scimitar')
	a = attack_roll(
		dscim['weapon']['stances']['chop'],
		{'weapon': dscim},
		Fighter(100, {}, []), 
		{'attack': 90},
		prayers=[],
		spell=None,
	)


	print(a)

	