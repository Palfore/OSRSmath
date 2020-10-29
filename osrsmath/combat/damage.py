from math import floor
from osrsmath.combat.items import ITEM_DATABASE
from pprint import pprint 

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
	salamanders = {'Black': 'Harralander', 'Red': 'Tarromin', 'Orange': 'Marrentill', 'Swamp': 'Guam'}
	for color, herb in salamanders.items():
		if f'{color} salamander' in equipment:
			if f'{herb} Tar' not in equipment:
				raise ValueError(f'{color} salamanders require {herb} tar as ammunition for all attack styles.')

			if stance['combat_style'] == 'scorch':
				stance['attack_style'] = 'aggressive'  # The database attack style is None, but should be aggressive for melee.
			else:
				raise ValueError(f'Salamanders can only deal melee damage using the Scorch combat style, not {stance["combat_style"]}.')

	if stance['attack_type'] not in ['slash', 'stab', 'crush']:
		raise ValueError(f'Invalid attack type in given stance: {stance}. Must be one of slash, stab, crush.')
	if stance['attack_style'] not in ['accurate', 'aggressive', 'controlled', 'defensive']:
		raise ValueError(f'Invalid attack style in given stance: {stance}. Must be one of accurate, aggressive, controlled, defensive.')

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

class Stance:
	def __init__(self, stance: dict):
		if stance is None:
			raise ValueError("The stance cannot be None.")
		self.stance = stance

	def get_combat_class(self):
		if 'ranged' in self.stance['experience']:
			return 'ranged'
		elif 'magic' in self.stance['experience']:
			return 'magic'
		elif any(self.stance['attack_type'] == melee_type for melee_type in ['stab', 'slash', 'crush']):
			return 'melee'
		else:
			raise LogicError(f"Something went wrong determining combat class for stance: {self.stance}")


	def can_train(self, skill):
		if skill not in ['attack', 'strength', 'defence', 'ranged', 'magic']:  # Should this include shared, maybe additional parameter
			raise ValueError(f"Only combat skills can be trained, not {skill}.")
		

def damage(stance, gear, opponent, effective_levels, prayers):
	combat_class = Stance(stance).get_combat_class()
	print(combat_class)
	assert prayers is None
	return melee_damage(
		stance,
		[i['name'] for i in gear.values()],
		opponent,
		effective_levels['strength'],
		sum(i['equipment']['melee_strength'] for i in gear.values()),
		prayer_multiplier=1.0
	)
	
class Player:
	EQUIPMENT_SLOTS = ['ammo', 'body', 'cape', 'feet', 'hands', 'head', 'legs', 'neck', 'ring', 'shield', 'weapon']

	def __init__(self, hitpoints: int, levels: dict, equipment: list):
		if hitpoints <= 0:
			raise ValueError(f"Player health must be positive, not {hitpoints}.")
		self.hitpoints = hitpoints
		self.levels = levels
		
		## Equip Items
		self.gear = {slot: None for slot in Player.EQUIPMENT_SLOTS}
		items = {name: ITEM_DATABASE.find(name) for name in equipment}
		slots_used = {item['equipment']['slot']: item['name'] for item in items.values()}
		
		# If the player has multiple items in the same slot, raise
		for slot in Player.EQUIPMENT_SLOTS:
			if list(slots_used.values()).count(slot) > 1:
				raise ValueError(f"Multiple items in {slot} slot")
		
		# If the player has a 2h and a weapon or shield, raise
		if ('2h' in slots_used and 'weapon' in slots_used):
			raise ValueError(f'''Cannot equip the 2h "{slots_used['2h']}" and the weapon "{slots_used['weapon']}".''')
		if('2h' in slots_used and 'shield' in slots_used):
			raise ValueError(f'''Cannot equip the 2h "{slots_used['2h']}" and the shield "{slots_used['shield']}".''')

		# Otherwise assign each item to the associated gear slot.
		for name, item in items.items():
			slot = item['equipment']['slot']
			self.gear[slot if slot != '2h' else 'weapon'] = item
		
		# If there is no weapon, equip a fist-like weapon (since unarmed isn't an actual weapon).
		if self.gear['weapon'] is None:
			self.gear['weapon'] = ITEM_DATABASE.find('Bruma torch')
		
		# Remove None slots so all gear is always valid.
		for slot in list(self.gear):
			if self.gear[slot] is None:
				del self.gear[slot]
		
		# Set a default stance to the first option.
		stances = self.get_stances()
		self.stance = stances[list(stances.keys())[0]]

	def get_stances(self):
		return self.gear['weapon']['weapon']['stances']

	def set_stance(self, combat_style):
		stances = self.get_stances()
		if combat_style not in stances:
			raise ValueError(f'Combat style "{combat_style}" not in stances: {list(stances.keys())}')
		self.stance = stances[combat_style]

	def max_hit(self, opponent):
		if self.stance is None:
			raise ValueError('Player stance has not been set. Check `Player.set_stance` and `Player.get_stances` for more info.')
		return damage(self.stance, self.gear, opponent, self.levels, prayers=None)



class Opponent:
	def __init__(self, attributes:list=None):
		self.attributes = attributes

	def has_attribute(self, attribute: str):
		allowed_attributes = ['kalphite', 'shade', 'dragonic', 'leafy', 'wilderness', 'demon', 'undead', 'slayer_task', 'vampyre']
		if attribute not in allowed_attributes:
			raise ValueError(f'The requested attribute check failed since {attribute} must be one of: {allowed_attributes}.')
		if self.attributes:
			return attribute in self.attributes
		return False



if __name__ == '__main__':
	# m = melee_damage({'attack_type': 'stab', 'attack_style': 'controlled'}, ['Crystal halberd'], Opponent(['slayer_task']), 
	# 	118, 168, 1.0
	# )
	# print(m)

	fighter = Player(90, {'strength': 50}, ["Black salamander", "Harralander tar"])
	pprint(fighter.get_stances())
	# print(fighter.stance)
	fighter.set_stance('scorch')
	print(fighter.max_hit(Opponent(['slayer_task'])))