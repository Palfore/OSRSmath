# Please fill me when you test things manually!
from osrsmath.skills.combat.fighter import Fighter, Player
from osrsmath.skills.combat.items import ITEM_DATABASE
import unittest

MAXED = {
	'attack': 99,
	'strength': 99,
	'defence': 99,
}

BASE_70s = {
	'attack': 70,
	'strength': 70,
	'defence': 70,
}

class MeleeGearCalculations(unittest.TestCase):
	# Make a test for various gear setups: basic and special.
	# def test_basic_player(self):
	# 	fighter1 = Fighter.from_player(Player(MAXED, [
	# 		'Dragon scimitar',
	# 		'Dragon sq shield',
	# 	]))
	# 	fighter2 = Fighter.from_player(Player(BASE_70s, [
	# 		'Dragon scimitar',
	# 		'Dragon sq shield',
	# 	]))

	# 	assert len(fighter1.attacks) == 1
	# 	attack1 = fighter1.attacks[0]
	# 	assert attack1.attack_type == 'slash'
	# 	assert attack1.attack_style == 'accurate'
	# 	self.assertEqual(attack1.max_hit(fighter1, fighter2), 22)
	# 	self.assertEqual(attack1.attack_roll(fighter1, fighter2), 14410)
	# 	self.assertEqual(attack1.defence_roll(fighter1, fighter2), 10179)
	# 	self.assertAlmostEqual(100*attack1.accuracy(fighter1, fighter2), 64.6762889)

	# 	assert len(fighter2.attacks) == 1
	# 	attack2 = fighter2.attacks[0]
	# 	assert attack2.attack_type == 'slash'
	# 	assert attack2.attack_style == 'accurate'
	# 	self.assertEqual(attack2.max_hit(fighter2, fighter1), 16)
	# 	self.assertEqual(attack2.attack_roll(fighter2, fighter1), 10611)
	# 	self.assertEqual(attack2.defence_roll(fighter2, fighter1), 13572)
	# 	self.assertAlmostEqual(100*attack2.accuracy(fighter2, fighter1), 39.0886318)


	def test_basic_npc(self):
		from osrsmath.skills.combat.monsters import MONSTER_DATABASE
		fighter1 = Fighter.from_player(Player(MAXED, [
			'Dragon scimitar',
			'Dragon sq shield',
		]))
		fighter2 = Fighter.from_monster(MONSTER_DATABASE.find('Abyssal demon'), 'stab')

		assert len(fighter1.attacks) == 1
		attack1 = fighter1.attacks[0]
		assert attack1.attack_type == 'slash'
		assert attack1.attack_style == 'accurate'
		self.assertEqual(attack1.max_hit(fighter1, fighter2), 22)
		self.assertEqual(attack1.attack_roll(fighter1, fighter2), 14410)
		self.assertEqual(attack1.defence_roll(fighter1, fighter2), 12096)
		self.assertAlmostEqual(100*attack1.accuracy(fighter1, fighter2), 58.0251197)

		
		assert len(fighter2.attacks) == 1
		attack2 = fighter2.attacks[0]
		assert attack2.attack_type == 'stab'
		assert attack2.attack_style == 'aggressive'
		self.assertEqual(attack2.max_hit(fighter2, fighter1), 8)
		# self.assertEqual(attack2.attack_roll(fighter2, fighter1), 10611)
		# self.assertEqual(attack2.defence_roll(fighter2, fighter1), 13572)
		# self.assertAlmostEqual(100*attack2.accuracy(fighter2, fighter1), 39.0886318)
		

	def test_void_melee(self):
		pass

	def test_salve(self):
		pass

	def test_slayer(self):
		pass
	

# class RangedGearCalculations(unittest.TestCase):
# 	# Make a test for various gear setups: basic and special.
# 	def test_normal(self):
# 		fighter1 = Fighter.from_player(Player({
# 				'attack': 99,
# 				'strength': 99,
# 				'defence': 99,
# 			}, [
# 				'Dragon scimitar'
# 			]
# 		))
# 		fighter2 = Fighter.from_player(Player({
# 				'attack': 70,
# 				'strength': 70,
# 				'defence': 70,
# 			}, [
# 				'Dragon scimitar'
# 			]
# 		))
		
# 		print([a.summary(fighter1, fighter2) for a in fighter1.attacks])
# 		print([a.summary(fighter2, fighter1) for a in fighter2.attacks])

# 		# self.almostEqual()

# 	def test_void_melee(self):
# 		pass

# 	def test_salve(self):
# 		pass

# 	def test_slayer(self):
# 		pass


# class MagicGearCalculations(unittest.TestCase):
# 	# Make a test for various gear setups: basic and special.
# 	def test_normal(self):
# 		fighter1 = Fighter.from_player(Player({
# 				'attack': 99,
# 				'strength': 99,
# 				'defence': 99,
# 			}, [
# 				'Dragon scimitar'
# 			]
# 		))
# 		fighter2 = Fighter.from_player(Player({
# 				'attack': 70,
# 				'strength': 70,
# 				'defence': 70,
# 			}, [
# 				'Dragon scimitar'
# 			]
# 		))
		
# 		print([a.summary(fighter1, fighter2) for a in fighter1.attacks])
# 		print([a.summary(fighter2, fighter1) for a in fighter2.attacks])

# 		# self.almostEqual()

# 	def test_void_melee(self):
# 		pass

# 	def test_salve(self):
# 		pass

# 	def test_slayer(self):
# 		pass
	