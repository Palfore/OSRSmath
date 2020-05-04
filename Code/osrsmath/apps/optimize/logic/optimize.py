from osrsmath.model.player import PlayerBuilder, get_equipment_by_name
from osrsmath.model.experience import xp_rate
from collections import defaultdict
from pprint import pprint
import itertools

import pathos.pools as pp
from multiprocessing import Value
import time

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
			if equipment['name'] in ignore:
				continue
			if equipment['name'] in adjustments:
				equipment['equipment']['requirements'] = adjustments[equipment['name']]

			# If you satisfy a requirement, you can make it None, and choose only from that group!
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
		if allow_controlled and stance['experience'] == 'shared':
			return True # This will probably fail with ranged/magic gear.
		return skill in stance['experience']

	def __init__(self, weapon):
		self.weapon = weapon

	def can_train(self, skill):
		return bool(self.get_skill_stances(skill))

	def get_skill_stances(self, skill, allow_controlled=False):
		return [stance for stance in self.weapon['weapon']['stances']
		           if Weapon.stance_can_train(stance, skill, allow_controlled)]

def is_better(A, B):
	""" Is A absolutely better than B?
		@param A Equipment stats eg: {'attack_crush': 53, ...}
		@param B Equipment stats """
	assert list(A.keys()) == list(B.keys())
	if list(A.values()) == list(B.values()):
		return False
	for a, b in zip(list(A.values()), list(B.values())):
		if b > a:
			return False
	return True

def get_equipment(slot_equipment, offensive_attribute):
	from osrsmath.apps.optimize.logic.utility import get_maximum_sets

	unique_equipment = []
	for equipment in slot_equipment:
		# Record equipment if you haven't seen anything with these offensive stats before.
		stats = get_offensive_bonuses(equipment, offensive_attribute)
		if stats not in [s for n, s, _ in unique_equipment]:
			unique_equipment.append((equipment['name'], stats, equipment))

	# Next, we want to search through this to see if any of these unique profiles are factually worse.
	# Eg: same stats except itemA.slash == 4, itemB.slash == 5, the itemA should be forgotten.
	# but if itemA.slash == 4, itemA.strength == 10 and item.B == 5, itemB.strength == 9, we can't
	# know which is better without evaluating, so keep them both.
	return [name for name, _, _ in get_maximum_sets(
		unique_equipment, getter=lambda x: x[1].values()  # x[1] -> stats
	)]


def get_sets(player_stats, defenders, ignore, adjustments, equipment_data, fixed_equipment=None):
	# Now I think I should seperate the weapon from the equipment, then select equipment based on
	# training skill & which (slash, stab, crush) can train that skill.

	items = get_offensive_melee_equipment(equipment_data)
	equipable_gear = get_equipable_gear(items, player_stats, ignore, adjustments)
	equipable_armour = {slot: equip for slot, equip in equipable_gear.items() if slot not in ['weapon', 'shield', '2h']}
	training_skill = 'attack'


	rune_scim = get_equipment_by_name('Rune scimitar')
	pprint(rune_scim)
	for stance in rune_scim['weapon']['stances']:
		print(stance)
	exit()
	# return
	# for attack_type in ['stab', 'slash', 'crush']
	# Get all weapons that can train the desired skill
	# weapons = []
	# for weapon in equipable_gear['weapon']:
	# 	stances = Weapon(weapon).get_skill_stances(training_skill)
	# 	if stances:
	# 		weapons.append((weapon, stances))

	# # Reduce weapons


	# for weapon, stances in weapons:
	# 	for stance in stances:
	# 		s = {slot: get_equipment(slot_eq, stance['attack_type']) for slot, slot_eq in equipable_armour.items()}
	# 		print(weapon['name'], stance['attack_type'], s, '\n')



	# reduced_equipment['weapon'] = []

	sets = []
	for attack in ['stab', 'slash', 'crush']:
		reduced_equipment = defaultdict(list)
		for i, (slot, slot_equipment) in enumerate(equipable_gear.items(), 1):
			reduced_equipment[slot] = list(set(
				get_equipment(slot_equipment, attack)
			))

		reduced_equipment = [ [(slot, e) for e in eqs] for slot, eqs in reduced_equipment.items()]
		sets += list(itertools.product(*list(reduced_equipment)[:-2]))  # Ignore last two slots (shield & weapon)
		sets += list(itertools.product(*list(reduced_equipment)[1:]))   # Ignore first slot (2h)



	print(len(sets))
	print(len(set(sets)))

	# exit()
	return [{ slot: eq for slot, eq in s if eq is not None} for s in sets]


# def create_set_effect(original, required_equipment):
# 		non_void = list(filter(lambda n: n[0] not in required_equipment, original))
# 		non_void.extend([(n, e) for n, e in required_equipment.items()])
# 		return tuple(non_void)

# 	# Adding Void Set
# 	void = {'body': 'Void knight top', 'legs': 'Void knight robe', 'hands': 'Void knight gloves', 'head': 'Void melee helm'}
# 	if all(meets_requirements(player_stats, get_equipment_by_name(e)) for e in void.values()):
# 		sets += list(set(create_set_effect(s, void) for s in sets))

# 	# Adding Obsidian Sets
# 	obsidian = {'head': 'Obsidian helmet', 'body': 'Obsidian platebody', 'legs': 'Obsidian platelegs', 'neck': 'Berserker necklace'}
# 	if all(meets_requirements(player_stats, get_equipment_by_name(e)) for e in obsidian.values()):
# 		for weapon in ['Toktz-xil-ek', 'Toktz-xil-ak', 'Tzhaar-ket-em', 'Tzhaar-ket-om', 'Tzhaar-ket-om (t)']:
# 			if meets_requirements(player_stats, get_equipment_by_name(weapon)):
# 				sets += list(set(create_set_effect(s, {
# 					**obsidian, **{'weapon': weapon}
# 				}) for s in sets))

# 	obsidian = {'neck': 'Berserker necklace'}
# 	if all(meets_requirements(player_stats, get_equipment_by_name(e)) for e in obsidian.values()):
# 		for weapon in ['toktz-xil-ek', 'toktz-xil-ak', 'tzhaar-ket-em', 'tzhaar-ket-om', 'tzhaar-ket-om (t)']:
# 			if meets_requirements(player_stats, get_equipment_by_name(weapon)):
# 				sets += list(set(create_set_effect(s, {
# 					**obsidian, **{'weapon': weapon}
# 				}) for s in sets))


def eval_set(player_stats: dict, training_skill, states, defenders, s, include_shared_xp=True):
	player = PlayerBuilder(player_stats).equip(s.values()).get()

	# Finds the best stance to train that skill for the given weapon.
	best_set, best_xp_rate, best_stance = best = (None, float('-inf'), None)
	for name, stance in player.get_stances().items():
		if stance['experience'] in ([training_skill] + (['shared'] if include_shared_xp else [])):
			player.combat_style = stance['combat_style']
			xp = xp_rate(
				stance['attack_type'],
				player.get_stats()['attack_speed'],
				states(player),
				defenders,
				'MarkovChain'
			)
			if xp > best[1]:
				best = (s, xp, player.combat_style)
	return best

class Eval:
	INTERVAL = 0.05  # How frequently the progress is updated (in seconds).
	completed = Value('i', 0)

	@classmethod
	def start(cls, f, items, callback):
		evaluator = Eval(f, len(items))
		values = cls.map(evaluator, items)
		evaluator.monitor_progress(callback)
		return list(values)

	@staticmethod
	def map(f, items):
		return pp.ProcessPool().imap(f, items)

	def __init__(self, f, num_items):
		self.num_items = num_items
		self.f = f
		with self.completed.get_lock():
			self.completed.value = 0

	def __call__(self, x):
		result = self.f(x)
		with self.completed.get_lock():
			self.completed.value += 1
		return result

	def monitor_progress(self, callback):
		callback(0)
		while self.completed.value < self.num_items:
			callback(self.completed.value/self.num_items*100)
			time.sleep(self.INTERVAL)
		callback(self.completed.value/self.num_items*100)

def get_best_set(player_stats: dict, training_skill, states, defenders, sets, include_shared_xp=True, progress_callback=None):
	""" Returns the equipment set that provides the highest experience rate for the training_skill.
		@param player_stats: {'attack': 40, ...}
		@param training_skill: 'attack'
		@param sets: [{'cape': 'Fire cape', ...}, {'cape': 'Legends cape', ...}, ...] """
	return max(Eval.start(
		lambda s: eval_set(player_stats, training_skill, states, defenders, s, include_shared_xp),
		sets,
		progress_callback
	), key = lambda x: x[1])  # x[1] -> xp rate