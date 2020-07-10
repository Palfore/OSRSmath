from osrsmath.apps.optimize.logic.utility import get_maximum_sets
from osrsmath.apps.optimize.logic.gear import (
	get_offensive_bonuses, get_offensive_melee_equipment, get_equipable_gear, meets_requirements, Weapon
)
from osrsmath.apps.optimize.logic.evaluation import mmap, eval_set
from osrsmath.combat.player import get_equipment_by_name
from collections import defaultdict
from pprint import pprint
import itertools

def remove(equipment, *slots):
	return {slot: equip for slot, equip in equipment.items() if slot not in slots}

def get_unique_equipment(attack_style, slot_equipment):
	''' Returns the names of the given equipment that are uniquely best, according to the attack_style. '''
	unique_equipment = []
	for equipment in slot_equipment:
		# Record equipment if you haven't seen anything with these offensive stats before.
		stats = get_offensive_bonuses(equipment, attack_style)
		if stats not in [s for n, s, _ in unique_equipment]:
			unique_equipment.append((equipment['name'], stats, equipment))

	# Next, we want to search through this to see if any of these unique profiles are factually worse.
	# Eg: same stats except itemA.slash == 4, itemB.slash == 5, the itemA should be forgotten.
	# but if itemA.slash == 4, itemA.strength == 10 and item.B == 5, itemB.strength == 9, we can't
	# know which is better without evaluating, so keep them both.
	return [equipment for name, _, equipment in get_maximum_sets(
		unique_equipment, getter=lambda x: x[1].values()  # x[1] -> stats
	)]

def get_armour_sets(attack_style, gear):
	''' Returns sets of load-outs, where each set is uniquely-maximal.
		@param attack_style The attack style which determines maximal-ness.
		@param gear The gear to consider.
		@note The gear should EXCLUDE (weapon&shield)/2h. '''
	if '2h' in gear:
		assert 'weapon' not in gear
		assert 'shield' not in gear
	if 'shield' in gear:
		assert '2h' not in gear

	reduced_equipment = [[
		(slot, e['name']) for e in get_unique_equipment(attack_style, equipment)
	] for slot, equipment in gear.items()]
	return list(itertools.product(*reduced_equipment))


class Solver:
	def __init__(self, training_skill, player_stats, ignore, adjustments, equipment_data, progress_callback=None):
		self.training_skill = training_skill
		self.player_stats = player_stats
		self.callback = progress_callback if progress_callback else lambda x: None
		self.gear = get_equipable_gear(
			get_offensive_melee_equipment(equipment_data), player_stats, ignore, adjustments
		)
		self.special_sets = []

	def add_special_set(self, weapons, gear):
		gear = {s: get_equipment_by_name(g) for s, g in gear.items()}
		if not all(meets_requirements(self.player_stats, g) for g in gear.values()):
			return
		if weapons:
			weapons = [get_equipment_by_name(w) for w in weapons]
			weapons = [w for w in weapons if meets_requirements(self.player_stats, w)]
			if not weapons:
				return
		self.special_sets.append((weapons, gear))

	def solve(self):
		attack_types = ['stab', 'slash', 'crush']
		equipment_sets = []
		M = len(attack_types)*(len(self.special_sets) + 1)
		i = 1
		for attack_type in attack_types:
			equipment_sets.extend(self.get_attack_sets(attack_type, []))
			self.callback(i/M*100); i += 1
			for weapons, special_gear in self.special_sets:
				if weapons:
					for weapon in weapons:
						equipment_sets.extend(self.get_special_sets_with_fixed_weapon(attack_type, weapon, special_gear))
				else:
					equipment_sets.extend(self.get_special_sets(attack_type, special_gear))
				self.callback(i/M*100); i += 1
		return [(a, {slot: eq for slot, eq in s if eq is not None}) for a, s in equipment_sets]

	def get_equipment_sets(self, attack_type, weapon_names, remove_slots):
		s = []
		for weapon in get_unique_equipment(attack_type, weapon_names):
			s.extend(self.get_weapon_sets(attack_type, weapon, remove_slots))
		return s

	def get_attack_sets(self, attack_type, remove_slots):
		return self.get_equipment_sets(attack_type, self.gear['weapon'], ['2h', 'weapon', *remove_slots]) +\
	     	    self.get_equipment_sets(attack_type, self.gear['2h'], ['2h', 'weapon', 'shield', *remove_slots])

	def get_special_sets(self, attack_type, special_gear):
		if not all(meets_requirements(self.player_stats, e) for e in special_gear.values()):
			return []
		return self.add_equipment_to_sets(self.get_attack_sets(attack_type, special_gear.keys()), special_gear)

	def get_special_sets_with_fixed_weapon(self, attack_type, weapon, special_gear):
		s = self.get_weapon_sets(attack_type, weapon, list(special_gear.keys()) + ['2h', 'weapon'])
		return self.add_equipment_to_sets(s, special_gear)

	def get_weapon_sets(self, attack_type, weapon, ignore):
		ignore += ['weapon', '2h'] if weapon['equipment']['slot'] == 'weapon' else ignore
		ignore += ['weapon', 'shield', '2h'] if weapon['equipment']['slot'] == '2h' else ignore
		armour = remove(self.gear, *ignore)
		s = []
		for stance in weapon['weapon']['stances']:
			if Weapon.stance_can_do(stance, self.training_skill, attack_type, allow_controlled=False):
				s.extend([
					(stance['combat_style'], [('weapon', weapon['name']), *a])
						for a in get_armour_sets(stance['attack_type'], armour)
				])
		return s

	def add_equipment_to_sets(self, original_sets, additional_equipment):
		return [
			(style, equipment + [(slot, e['name']) for slot, e in additional_equipment.items()])
				for style, equipment in original_sets
		]


def get_sets(training_skill, player_stats, defenders, ignore, adjustments, equipment_data, considered_sets, progress_callback=None):
	sets = {
		'void_knight': (None, {
				'body': 'Void knight top',
				'legs': 'Void knight robe',
				'hands': 'Void knight gloves',
				'head': 'Void melee helm'
		}),
		'elite_void': (None, {
				'body': 'Elite void top',
				'legs': 'Elite void robe',
				'hands': 'Void knight gloves',
				'head': 'Void melee helm'
		}),
		'obsidian': ([
				'Toktz-xil-ek', 'Toktz-xil-ak', 'Tzhaar-ket-em', 'Tzhaar-ket-om', 'Tzhaar-ket-om (t)'
			], {
				'head': 'Obsidian helmet',
				'body': 'Obsidian platebody',
				'legs': 'Obsidian platelegs',
				'neck': 'Berserker necklace'
		}),
		'berserker_necklace': ([
				'Toktz-xil-ek', 'Toktz-xil-ak', 'Tzhaar-ket-em', 'Tzhaar-ket-om', 'Tzhaar-ket-om (t)'
			], {
				'neck': 'Berserker necklace'
		}),
		'slayer_helm': (None, {
			'head': 'Slayer helmet'
		}),
		'salve_amulet': (None, {
			'neck': 'Salve amulet'
		}),
		'dharok': ([
			"Dharok's greataxe"
			], {
				'head': "Dharok's helm",
				'body': "Dharok's platebody",
				'legs': "Dharok's platelegs",
			}
		)
	}
	solver = Solver(training_skill, player_stats, ignore, adjustments, equipment_data, progress_callback)
	for name, special_set in sets.items():
		if name in considered_sets:
			print(name)
			solver.add_special_set(*special_set)
	return solver.solve()

def get_best_set(player_stats: dict, training_skill, states, defenders, sets, include_shared_xp=True, progress_callback=None, num_cores=0):
	""" Returns the equipment set that provides the highest experience rate for the training_skill.
		@param player_stats: {'attack': 40, ...}
		@param training_skill: 'attack'
		@param sets: [{'cape': 'Fire cape', ...}, {'cape': 'Legends cape', ...}, ...] """
	sets = mmap(
		lambda s: eval_set(player_stats, training_skill, states, defenders, s, include_shared_xp),
		sets,
		progress_callback if progress_callback else lambda x: None,
		num_cores=num_cores
	)
	if not sets:
		return None, 0, None

	return max(sets, key=lambda x: x[1]), [s[1] for s in sets]  # x[1] -> xp rate
