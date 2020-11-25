from osrsmath.combat.items import ITEM_DATABASE
from osrsmath.combat.damage import damage

class NoAmmoPolicyFoundError(ValueError):
	pass

def satisfies_bow_requirements(gear):
	# Barbarian assault ammo is ignored.
	def UPTO(level, projectile):
		""" Returns a list of arrows that can be used by a bow, whose best usable arrow is made of the given metal. """
		dart_metals      = ["Bronze", "Iron", "Steel", "Black", "Mithril", "Adamant", "Rune", "Dragon"]
		knife_metals     = ["Bronze", "Iron", "Steel", "Black", "Mithril", "Adamant", "Rune", "Dragon"]
		thrownaxe_metals = ["Bronze", "Iron", "Steel",          "Mithril", "Adamant", "Rune", "Dragon"]
		projectiles = {
			"arrows": {
				"Bronze"  : ["Bronze arrows", "Bronze fire arrows"],
				"Iron"    : ["Iron arrows", "Iron fire arrows"],
				"Steel"   : ["Steel arrows", "Steel fire arrows"],
				"Mithril" : ["Mithril arrows", "Mithril fire arrows"],
				"Adamant" : ["Adamant arrows", "Adamant fire arrows"],
				"Rune"    : ["Rune arrows", "Rune fire arrows", "Ice arrows"],
				"Amethyst": ["Amethyst arrows", "Amethyst fire arrows", "Broad arrows"],
				"Dragon"  : ["Dragon arrows", "Dragon fire arrows"],
			},
			"bolts": {
				"Bronze" : ["Bronze bolts", "Opal bolts (e)", "Barbed bolts"],
				"Blurite": ["Blurite bolts", "Jade bolts (e)"],
				"Iron"   : ["Iron bolts", "Pearl bolts (e)", "Silver bolts"],
				"Steel"  : ["Steel bolts", "Topaz bolts (e)"],
				"Mithril": ["Mithril bolts", "Sapphire bolts (e)", "Emerald bolts (e)"],
				"Adamant": ["Adamant bolts", "Ruby bolts (e)", "Diamond bolts (e)"],
				"Rune"   : ["Runite bolts", "Dragonstone bolts (e)", "Onyx bolts (e)", "Broad bolts", "Amethyst broad bolts"],
				"Dragon" : ["Dragon bolts", "Opal dragon bolts (e)", "Jade dragon bolts (e)", "Pearl dragon bolts (e)", 
				    "Topaz dragon bolts (e)", "Sapphire dragon bolts (e)", "Emerald dragon bolts (e)", 
				    "Ruby dragon bolts (e)", "Diamond dragon bolts (e)", "Dragonstone dragon bolts (e)", 
				    "Onyx dragon bolts (e)"],
			},
			"darts": {
				None: [] + 
					[f"{m} dart" for m in dart_metals] + 
					[f"{m} dart(p)" for m in dart_metals] + 
					[f"{m} dart(p+)" for m in dart_metals] + 
					[f"{m} dart(p++)" for m in dart_metals]
			},
			"knives": {
				None: [] + 
					[f"{m} knife" for m in dart_metals] + 
					[f"{m} knife(p)" for m in dart_metals] + 
					[f"{m} knife(p+)" for m in dart_metals] + 
					[f"{m} knife(p++)" for m in dart_metals]
			},
			"thrownaxe": {
				None: [f"{m} thrownaxe" for m in thrownaxe_metals] + ["Morrigan's throwing axe"]
			}
		}
		return sum([
			items for i, (metal, items) in enumerate(projectiles[projectile].items())
			if i >= list(projectiles[projectile].keys()).index(level)
		], [])

	has_ammo = 'ammo' in gear
	ammo = gear['ammo'] if has_ammo else None
	policies =  {
		"CANNOT_ATTACK": {
			'valid': False,
			'weapons': ["Craw's bow (u)"]
		},
		"NO_AMMO": {
			'valid': (not has_ammo) or ('blessing' in ammo['name']) or ('grapple' in ammo['name']),
			'weapons': [
				# Bows
				"New crystal bow (i)", "Starter bow", "Craw's bow", "Corrupted bow (basic)", "Corrupted bow (attuned)",
				"Corrupted bow (perfected)", "Crystal bow (basic)", "Crystal bow (attuned)", "Crystal bow (perfected)",
				"Crystal bow", "Crystal bow",
				# Crossbows (there are none)
				# Thrown
				*UPTO(None, "darts"),
				*UPTO(None, "knives"),
				*UPTO(None, "thrownaxe"),
				"Morrigan's javelin",
				"Chinchompa", "Red chinchompa", "Black chinchompa",
				"Toktz-xil-ul", "Holy water", "Mud pie",
			],
		},
		"OGRE_ARROWS": {
			'valid': has_ammo and ammo['name'] == 'Ogre arrow',
			'weapons': ["Ogre bow"],
		},
		"BRUTAL_ARROWS": {
			'valid': has_ammo and ammo['name'].endswith('brutal'),
			'weapons': ["Comp ogre bow"],
		},
		"TRAINING_ARROWS": {
			'valid': has_ammo and ammo['name'] == 'Training arrows',
			'weapons': ["Training bow"],
		},
		"UPTO_IRON_ARROWS": {
			'valid': has_ammo and ammo['name'] in UPTO("Iron", "arrows"),
			'weapons': ["Cursed goblin bow", "Rain bow", "Shortbow", "Longbow"],
		},
		"UPTO_STEEL_ARROWS": {
			'valid': has_ammo and ammo['name'] in UPTO("Steel", "arrows"),
			'weapons': ["Signed oak bow", "Oak shortbow", "Oak longbow"],
		},
		"UPTO_MITHRIL_ARROWS": {
			'valid': has_ammo and ammo['name'] in UPTO("Mithril", "arrows"),
			'weapons': ["Willow longbow", "Willow shortbow", "Willow comp bow"],
		},
		"UPTO_ADAMANT_ARROWS": {
			'valid': has_ammo and ammo['name'] in UPTO("Adamant", "arrows"),
			'weapons': ["Maple longbow", "Maple shortbow"],
		},
		"UPTO_RUNE_ARROWS": {
			'valid': has_ammo and ammo['name'] in UPTO("Rune", "arrows"),
			'weapons': ["Yew longbow", "Yew shortbow", "Yew comp bow"],
		},
		"UPTO_AMETHYST_ARROWS": {
			'valid': has_ammo and ammo['name'] in UPTO("Amethyst", "arrows"),
			'weapons': ["Magic shortbow", "Magic longbow", "Magic comp bow", "Seercull", "Magic shortbow (i)"],
		},
		"UPTO_DRAGON_ARROWS": {
			'valid': has_ammo and ammo['name'] in UPTO("Dragon", "arrows"),
			'weapons': ["3rd age bow", "Dark bow", "Twisted bow"],
		},

		"BONE_BOLTS": {
			'valid': has_ammo and ammo['name'] == "Bone bolts",
			'weapons': ['Dorgeshuun crossbow']
		},
		"BOLT_RACKS": {
			'valid': has_ammo and ammo['name'] == "Bolt racks",
			'weapons': ["Karil's crossbow", "Karil's crossbow 100", "Karil's crossbow 75", "Karil's crossbow 50", "Karil's crossbow 25"]
		},
		"KEBIT_BOLTS" :{
			'valid': has_ammo and ammo['name'] in ["Kebbit bolts", "Long kebbit bolts"],
			'weapons': ["Hunters' crossbow"]
		},
		"UPTO_BRONZE_BOLTS": {
			'valid': has_ammo and ammo['name'] in UPTO("Iron", "bolts"),
			'weapons': ["Crossbow", "Phoenix crossbow", "Bronze crossbow"],
		},
		"UPTO_BLURITE_BOLTS": {
			'valid': has_ammo and ammo['name'] in UPTO("Iron", "bolts"),
			'weapons': ["Blurite crossbow"],
		},
		"UPTO_IRON_BOLTS": {
			'valid': has_ammo and ammo['name'] in UPTO("Iron", "bolts"),
			'weapons': ["Iron crossbow"],
		},
		"UPTO_STEEL_BOLTS": {
			'valid': has_ammo and ammo['name'] in UPTO("Steel", "bolts"),
			'weapons': ["Steel crossbow"],
		},
		"UPTO_MITHRIL_BOLTS": {
			'valid': has_ammo and ammo['name'] in UPTO("Mithril", "bolts"),
			'weapons': ["Mithril crossbow"],
		},
		"UPTO_ADAMANT_BOLTS": {
			'valid': has_ammo and ammo['name'] in UPTO("Adamant", "bolts"),
			'weapons': ["Adamant crossbow"],
		},
		"UPTO_RUNE_BOLTS": {
			'valid': has_ammo and ammo['name'] in UPTO("Rune", "bolts"),
			'weapons': ["Rune crossbow"],
		},
		"UPTO_DRAGON_BOLTS": {
			'valid': has_ammo and ammo['name'] in UPTO("Dragon", "bolts"),
			'weapons': ["Dragon crossbow", "Armadyl crossbow", "Dragon hunter crossbow"],
		},

		"JAVELINS": {  # Morrigan's is the only jav that can be used w/o a ballista.
			'valid': has_ammo and ammo['name'].endswith('javelin') and ammo['name'] != "Morrigan's javelin",
			'weapons': ["Light ballista", "Heavy ballista"]
		},

		"GUAM_TAR": {
			'valid': has_ammo and ammo['name'] == "Guam tar",
			'weapons': ['Swamp lizard']
		},
		"MARRENTILL_TAR": {
			'valid': has_ammo and ammo['name'] == "Marrentill tar",
			'weapons': ['Orange salamander']
		},
		"TARROMIN_TAR": {
			'valid': has_ammo and ammo['name'] == "Tarromin tar",
			'weapons': ['Red salamander']
		},
		"HARRALANDER_TAR": {
			'valid': has_ammo and ammo['name'] == "Harralander tar",
			'weapons': ['Black salamander']
		},

		"DARTS": {
			'valid': has_ammo and ammo['name'].endswith('dart'),
			'weapons': ['Toxic blowpipe']
		}
	}

	weapon = gear['weapon']
	for policy, details in policies.items():
		if weapon['name'] in details['weapons']:
			return details['valid']
	raise NoAmmoPolicyFoundError(f'''The ammo policy could not be found for the ranged weapon "{weapon['name']}".''')

def can_attack(stance, gear):
	if stance['experience'] is None:
		return False
	
	if stance['combat_class'] == 'ranged':
		return satisfies_bow_requirements(gear)
	return False
	

class Fighter:
	EQUIPMENT_SLOTS = ['ammo', 'body', 'cape', 'feet', 'hands', 'head', 'legs', 'neck', 'ring', 'shield', 'weapon']
	ALLOWED_ATTRIBUTES = ['kalphite', 'shade', 'dragonic', 'leafy', 'wilderness', 'demon', 
	                      'undead', 'slayer_task', 'vampyre', 'charge']
	
	def __init__(self, hitpoints: int, levels: dict, equipment: list, attributes: list=None):
		if hitpoints <= 0:
			raise ValueError(f"Fighter health must be positive, not {hitpoints}.")
		self.hitpoints = hitpoints
		self.levels = levels

		## Assign Attributes
		attributes = attributes if attributes is not None else []
		for a in attributes:
			if a not in self.ALLOWED_ATTRIBUTES:
				raise ValueError(f'The attribute "{a}" does not exist. Must be one of: {self.ALLOWED_ATTRIBUTES}.')
		self.attributes = attributes
		
		## Equip Items
		self.gear = {slot: None for slot in self.EQUIPMENT_SLOTS}
		items = {name: ITEM_DATABASE.find(name) for name in equipment}
		
		# If the player has a 2h and a weapon or shield, raise
		slots_used = {item['equipment']['slot']: item['name'] for item in items.values()}
		if ('2h' in slots_used and 'weapon' in slots_used):
			raise ValueError(f'''Cannot equip the 2h "{slots_used['2h']}" and the weapon "{slots_used['weapon']}".''')
		if('2h' in slots_used and 'shield' in slots_used):
			raise ValueError(f'''Cannot equip the 2h "{slots_used['2h']}" and the shield "{slots_used['shield']}".''')

		# Otherwise assign each item to the associated gear slot.
		for name, item in items.items():
			slot = item['equipment']['slot']
			slot = slot if slot != '2h' else 'weapon'
			if self.gear[slot] is not None:
				raise ValueError(f"Multiple items in {slot} slot: {self.gear[slot]['name']} and {name}")
			self.gear[slot] = item
		
		# If there is no weapon, equip a fist-like weapon (since unarmed isn't an actual weapon).
		if self.gear['weapon'] is None:
			self.gear['weapon'] = ITEM_DATABASE.find('Unarmed')
		
		# Remove None slots so all gear is always valid.
		for slot in list(self.gear):
			if self.gear[slot] is None:
				del self.gear[slot]
		
		# Set a default stance to the first option.
		self.set_stance(list(self.get_stances().keys())[0])

	def has_attribute(self, attribute: str):
		if attribute not in self.ALLOWED_ATTRIBUTES:
			raise ValueError(f'The requested attribute check failed since {attribute} must be one of: {ALLOWED_ATTRIBUTES}.')
		if self.attributes:
			return attribute in self.attributes
		return False

	def get_stances(self):
		return self.gear['weapon']['weapon']['stances']

	def set_stance(self, combat_style):
		stances = self.get_stances()
		if combat_style not in stances:
			raise ValueError(f'Combat style "{combat_style}" not in stances: {list(stances.keys())}')
		self.stance = stances[combat_style]

	def can_train(self, skill, shared=False):
		if not self.can_attack():
			return False
		if skill not in ['attack', 'strength', 'defence', 'ranged', 'magic']:  # Should this include shared, maybe additional parameter
			raise ValueError(f"Only combat skills can be trained, not {skill}.")
		raise NotImplementedError

	def can_attack(self):
		return can_attack(self.stance, self.gear)

	def max_hit(self, opponent):
		if self.stance is None:
			raise ValueError('Fighter stance has not been set. Check `Fighter.set_stance` and `Fighter.get_stances` for more info.')
		return damage(self.stance, self.gear, opponent, self.levels, prayers=None)

	def accuracy(self, opponent):
		return 1.0

	def damage_distribution(self, opponent):
		m = self.max_hit(opponent)
		a = self.accuracy(opponent)
		return {**{
			0: 1 - a * m / (m + 1)},
			**{
				c: a / (m + 1) for c in range(1, m+1)
			}
		}


if __name__ == '__main__':
	from pprint import pprint
	# from osrsmath.combat.damage import CannotAttackException, ExcludedClassException
	m = damage(ITEM_DATABASE.find("Dawnbringer")['weapon']['stances']['accurate'], 
		{'weapon': ITEM_DATABASE.find("Dawnbringer")}, 
		Fighter(100, {}, []), {'magic': 90}, prayers=[], spell=None)
	print(m)

	weapon = ITEM_DATABASE.find('Slayer\'s staff (e)')
	m = damage(weapon['weapon']['stances']['spell'], {
			'weapon': weapon, None: ITEM_DATABASE.create_dummy({
				'magic_attack': 40,
				'magic_damage': 0.0,
			})
		}, Fighter(100, {}, []), {
			'magic': 70,
		}, [], spell="Magic dart")
	print(m)

	# opponent = Fighter(100, {'strength': 50}, [], attributes=['kalphite'])
	# for weapon_id in ITEM_DATABASE.get_slot('weapon') + ITEM_DATABASE.get_slot('2h'):
	# 	weapon = ITEM_DATABASE.get(weapon_id)['name']
	# 	fighter = Fighter(90, {'strength': 50}, [weapon, 'Mithril arrow'])
	# 	for stance in fighter.get_stances():
	# 		fighter.set_stance(stance)
	# 		try:
	# 			m = fighter.max_hit(opponent)
	# 			fighter.can_attack()
	# 		# 	if m == -1:
	# 		# 		continue
	# 		# 	# if not isinstance(m, int):
	# 		# 	# if m != None and m != 0:
	# 		# 	print(stance, weapon, m)
	# 		except CannotAttackException as e:
	# 			print('Skipping', stance, weapon, f"due to {str(e)}")
	# 		except ExcludedClassException as e:
	# 			pass

	# for weapon_id in ITEM_DATABASE.get_slot('weapon') + ITEM_DATABASE.get_slot('2h'):
	# 	weapon = ITEM_DATABASE.get(weapon_id)
	# 	if weapon['weapon']['weapon_type'] == 'bows':
	# 		print(weapon['name'])
	# exit()
	

	# for weapon_id in ITEM_DATABASE.get_slot('weapon') + ITEM_DATABASE.get_slot('2h'):
	# 	weapon = ITEM_DATABASE.get(weapon_id)
	# 	for ammo_id in ITEM_DATABASE.get_slot('ammo'):
	# 		ammo = ITEM_DATABASE.get(ammo_id)
	# 		# pprint(ammo)
	# 		a = can_attack({'experience': True, 'combat_class': 'ranged'}, {
	# 			'weapon': weapon,
	# 			'ammo': ammo
	# 		})
	# 		if a:
	# 			print(weapon['name'], ammo['name'], a)