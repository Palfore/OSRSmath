from typing import Callable, Union

class SpecialEquipment:
	def __init__(self, bonuses: dict, requires: Union[Callable, dict, None]=None):
		self.melee_damage_pre = lambda _: 1
		self.melee_accuracy_pre = lambda _: 1
		self.ranged_damage_pre = lambda _: 1
		self.ranged_accuracy_pre = lambda _: 1
		self.magic_damage_add = lambda _: 0
		self.magic_damage_pre = lambda _: 0
		self.magic_accuracy_pre = lambda _: 1

		self.melee_damage_post = lambda _: 1
		self.melee_accuracy_post = lambda _: 1
		self.ranged_damage_post = lambda _: 1
		self.ranged_accuracy_post = lambda _: 1
		self.magic_damage_add = lambda _: 0
		self.magic_damage_post = lambda _: 0
		self.magic_accuracy_post = lambda _: 1
		for k, v in bonuses.items():
			if not hasattr(v, '__call__'):
				setattr(self, k, lambda _: v)
			else:
				setattr(self, k, lambda arena: v(arena))
		self.requires = requires

	def applies(self, arena):
		if self.requires is None:
			return True
		elif isinstance(self.requires, dict):
			equipment = arena.fighter.loadout.equipment
			valid = True
			for slot, item_name in self.requires.items():
				if slot not in equipment:
					return False
				elif equipment[slot] is None:
					return False
				elif isinstance(item_name, list) or isinstance(item_name, tuple):
					item_names = item_name
					if not any(equipment.name.lower() != name.lower() for name in item_names):
						return False
				elif isinstance(item_name, str):
					if item_name.lower() not in equipment[slot].name.lower():
						return False
				else:
					raise ValueError(f'Invalid type for special set requirement: {type(self.requires)}')
			return True
		elif hasattr(self.requires, '__call__'):
			return self.requires(arena)
		else:
			raise ValueError(f'SpecialEquipment requirements must be either a dict or function, not {type(requirements)}')



SPECIAL_ITEMS = {
	
}

SPECIAL_SETS = {
	### VOID #########################
	'void melee': SpecialEquipment({
			'melee_damage_pre': 1.1,
			'melee_accuracy_pre': 1.1
		}, requires={
			'head': 'Void melee helm',
			'body': 'Void knight top',
			'legs': 'Void knight robe',
			'hands': 'Void knight gloves',
	}),
	'void ranger': SpecialEquipment({
			'ranged_damage_pre': 1.1,
			'ranged_accuracy_pre': 1.1
		}, requires={
			'head': 'Void ranger helm',
			'body': 'Void knight top',
			'legs': 'Void knight robe',
			'hands': 'Void knight gloves',
	}),
	'void mage': SpecialEquipment({
			'magic_accuracy_pre': 1.45,
		}, requires={
			'head': 'Void mage helm',
			'body': 'Void knight top',
			'legs': 'Void knight robe',
			'hands': 'Void knight gloves',
	}),
	'void elite melee': SpecialEquipment({
			'melee_damage_pre': 1.1,
			'melee_accuracy_pre': 1.1
		}, requires={
			'head': 'Void melee helm',
			'body': 'Elite void top',
			'legs': 'Elite void robe',
			'hands': 'Void knight gloves',
	}),
	'void elite ranger': SpecialEquipment({
			'ranged_damage_pre': 1.1,
			'ranged_accuracy_pre': 1.1
		}, requires={
			'head': 'Void ranger helm',
			'body': 'Elite void top',
			'legs': 'Elite void robe',
			'hands': 'Void knight gloves',
	}),
	'void elite mage': SpecialEquipment({
			'magic_accuracy_pre': 1.45,
		}, requires={
			'head': 'Void mage helm',
			'body': 'Elite void top',
			'legs': 'Elite void robe',
			'hands': 'Void knight gloves',
	}),

	'inquisitors': SpecialEquipment({ 
			# nothing since the individual items in SPECIAL_ITEMS takes care of this.
		}, requires=lambda arena: arena.fighter.get_attack_style() == 'crush' and \
			len(n for n in arena.fighter.loadout.get_names() if n != "inquisitor's mace" and n.startswith('inquisitors')) == 3
	),

	### BARROWS ##################################
	'dharok': SpecialEquipment({
			'melee_damage_post': lambda arena: 1 + 0.01*(arena.fighter.levels['hitpoints'] - arena.fighter.current_health)
		}, requires={
			'head': "Dharok's helm",
			'body': "Dharok's platebody",
			'legs': "Dharok's platelegs",
			'weapon': "Dharok's greataxe",
		}
	),

}

SPECIAL_EQUIPMENT = {
	
	### SLAYER HELM #########################
	'black mask': SpecialEquipment({
			'melee_damage_pre': 7/6,
			'melee_accuracy_pre': 7/6,
		}, requires=lambda arena: 'head' in arena.fighter.loadout.equipment and arena.fighter.loadout.equipment['head'].name == 'black mask' and arena.on_slayer_task
	),
	'black mask (i)': SpecialEquipment({
			'melee_damage_pre': 7/6,
			'melee_accuracy_pre': 7/6,
			'ranged_damage_pre': 1.15,
			'ranged_accuracy_pre': 1.15,
			'magic_damage_pre': 15,
			'magic_accuracy_pre': 1.15,
		}, requires=lambda arena: 'head' in arena.fighter.loadout.equipment and arena.fighter.loadout.equipment['head'].name == 'black mask (i)' and arena.on_slayer_task
	),
	'slayer helmet': SpecialEquipment({
			'melee_damage_pre': 7/6,
			'melee_accuracy_pre': 7/6,
		}, requires=lambda arena: 'head' in arena.fighter.loadout.equipment and arena.fighter.loadout.equipment['head'].name == 'slayer helmet' and arena.on_slayer_task
	),
	'slayer helmet (i)': SpecialEquipment({
			'melee_damage_pre': 7/6,
			'melee_accuracy_pre': 7/6,
			'ranged_damage_pre': 1.15,
			'ranged_accuracy_pre': 1.15,
			'magic_damage_pre': 15,
			'magic_accuracy_pre': 1.15,
		}, requires=lambda arena: 'head' in arena.fighter.loadout.equipment and arena.fighter.loadout.equipment['head'].name == 'slayer helmet (i)' and arena.on_slayer_task
	),

	### SALVE AMULET #########################
	# This is very confusing, not sure if I have these all right: https://oldschool.runescape.wiki/w/Salve_amulet
	'salve amulet': SpecialEquipment({
			'melee_damage_pre': 7/6,
			'melee_accuracy_pre': 7/6,
		}, requires={
			'neck': 'salve amulet',
	}),
	'salve amulet (i)': SpecialEquipment({
			'melee_damage_pre': 7/6,
			'melee_accuracy_pre': 7/6,
			'ranged_damage_pre': 7/6,
			'ranged_accuracy_pre': 7/6,
			'magic_accuracy_pre': 1.15,
			'magic_damage_pre': 15,
		}, requires={
			'neck': 'salve amulet (i)',
	}),
	'salve amulet (e)': SpecialEquipment({
			'melee_damage_pre': 1.2,
			'melee_accuracy_pre': 1.2,
		}, requires={
			'neck': 'salve amulet (e)',
	}),
	'salve amulet (ei)': SpecialEquipment({
			'melee_damage_pre': 1.2,
			'melee_accuracy_pre': 1.2,
			'ranged_damage_pre': 1.2,
			'ranged_accuracy_pre': 1.2,
			'magic_damage_pre': 20,
			'magic_accuracy_pre': 1.2, 
		}, requires={
			'neck': 'salve amulet (ei)',
	}),

	### INQUISITORS ##################################
	'inquisitors1': SpecialEquipment({
			'melee_damage_pre': 1.005,
			'melee_accuracy_pre': 1.005,
		}, requires=lambda arena: arena.fighter.get_attack_style() == 'crush' and \
			len(n for n in arena.fighter.loadout.get_names() if n != "inquisitor's mace" and n.startswith('inquisitors')) == 1
	),
	'inquisitors2': SpecialEquipment({
			'melee_damage_pre': 1.01,
			'melee_accuracy_pre': 1.01,
		}, requires=lambda arena: arena.fighter.get_attack_style() == 'crush' and \
			len(n for n in arena.fighter.loadout.get_names() if n != "inquisitor's mace" and n.startswith('inquisitors')) == 2
	),
	'inquisitors3': SpecialEquipment({
			'melee_damage_pre': 1.025,
			'melee_accuracy_pre': 1.025,
		}, requires=lambda arena: arena.fighter.get_attack_style() == 'crush' and \
			len(n for n in arena.fighter.loadout.get_names() if n != "inquisitor's mace" and n.startswith('inquisitors')) == 3
	),

}

# set effects
# void
# dharok
# Inquisitors
# Obsidian armor


# Inquisitors
# slayer helm 
# Salve bonus (ranged/melee)
# Slayer bonus (ranged/melee)
# Arclight
# silverlight?
# Darklight
# Leaf-bladed battleaxe
# Dragon hunter lance
# Craws's/Viggora's
# Berserker Necklace
# Granite hammer
