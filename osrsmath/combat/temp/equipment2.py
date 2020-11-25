SLOTS = ['head', 'cape',  'neck', 'ammo', 'weapon', 'body', 'shield', 'legs', 'hands', 'feet', 'ring']

class Item:
	""" Models an equipable in-game item. """

	def __init__(self, database_entry: dict):
		self.entry = database_entry

	@property
	def name(self):
		return self._name

	@property
	def ID(self):
		return self._ID

	@property
	def slot(self):
		return self._slot
	
	@property
	def attack_stab(self):
		return self._attack_stab
	
	@property
	def attack_slash(self):
		return self._attack_slash
	
	@property
	def attack_crush(self):
		return self._attack_crush

	@property
	def attack_ranged(self):
		return self._attack_ranged
	
	@property
	def attack_magic(self):
		return self._attack_magic

	@property
	def defence_stab(self):
		return self._defence_stab
	
	@property
	def defence_slash(self):
		return self._defence_slash
	
	@property
	def defence_crush(self):
		return self._defence_crush

	@property
	def defence_ranged(self):
		return self._defence_ranged
	
	@property
	def defence_magic(self):
		return self._defence_magic

	@property
	def warrior_strength(self):
		return self._warrior_strength

	@property
	def ranged_strength(self):
		return self.ranged_strength
	
	@property
	def magic_strength(self):
		return self._magic_strength

	@property
	def weight(self):
		return self._weight
	
	@property
	def prayer(self):
		return self._prayer

class Fighter:
	def get_damage_distribution(c=False):


if __name__ == '__main__':
	arena = Arena(Fighter(levels), Monsters.find('Black knight', attributes=('wildy',)))
	arena.fighter.equip(name='Dragon Scimitar', slot='weapon')
	arena.fighter.set_stance('slash')
	m, a = arena.fighter.get_damage_distribution(c=False)
	M, A = arena.opponent.get_damage_distribution(c=False)
	L = Arena.get_expected_length_of_fight(a, m, arena.fighter.health)
	P_win = Arena.get_probabilty_of_win(a, m, arena.fighter.health, A, M, arena.opponent.health)
	print(m, a, L, P_win)
	
	