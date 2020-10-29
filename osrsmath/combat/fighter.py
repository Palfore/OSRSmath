from osrsmath.combat.items import ITEM_DATABASE
from osrsmath.combat.damage import damage
	
class Fighter:
	EQUIPMENT_SLOTS = ['ammo', 'body', 'cape', 'feet', 'hands', 'head', 'legs', 'neck', 'ring', 'shield', 'weapon']
	ALLOWED_ATTRIBUTES = ['kalphite', 'shade', 'dragonic', 'leafy', 'wilderness', 'demon', 'undead', 'slayer_task', 'vampyre']
	
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
		if self.stance['experience'] is None:
			return False
		return True

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
			0: 1 - a * m / (m + 1)}, **{
			c: a / (m + 1) for c in range(1, m+1)
		}}


if __name__ == '__main__':
	from osrsmath.combat.damage import CannotAttackException
	opponent = Fighter(100, {'strength': 50}, [], attributes=['kalphite'])
	for weapon_id in ITEM_DATABASE.get_slot('weapon') + ITEM_DATABASE.get_slot('2h'):
		weapon = ITEM_DATABASE.get(weapon_id)['name']
		fighter = Fighter(90, {'strength': 50}, [weapon])
		for stance in fighter.get_stances():
			fighter.set_stance(stance)
			try:
				m = fighter.max_hit(opponent)
				if m == -1:
					continue
				# if not isinstance(m, int):
				# if m != None and m != 0:
				print(stance, weapon, m)
			except CannotAttackException as e:
				print('Skipping', stance, weapon, f"due to {str(e)}")