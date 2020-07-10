from osrsmath.combat.damage import *
from osrsmath.combat.boosts import *
import unittest

class TestAccuracy(unittest.TestCase):
	def test_accuracy_from_melee_unit_test(self):
		self.assertAlmostEqual(accuracy(35_000, 12_096), 0.82717636639)


class TestMelee(unittest.TestCase):
	# https://www.osrsbox.com/blog/2019/01/22/calculating-melee-dps-in-osrs/

	a, s = 97, 99

	def test_max_hit(self):
		self.assertEqual(
			Melee().max_hit(133, self.s, Potions.super(self.s), Prayers.piety('strength'), Equipment.black_mask()['strength'], 0, 1, 1),
			54
		)

	def test_attack_roll(self):
		self.assertEqual(
			Melee().max_attack_roll(136, self.a, Potions.super(self.a), Prayers.piety('attack'), 1, 3, Equipment.black_mask()['attack']),
			35_000  # Not sure why black_mask is multiplier here, but other for strength?
		)

	def test_defence_roll(self):
		self.assertEqual(
			Melee().max_defence_roll(20, 135, 0, 1, 1, 1, 1),
			12_096
		)



class TestRange(unittest.TestCase):
	# https://www.osrsbox.com/blog/2019/01/22/calculating-melee-dps-in-osrs/

	r = 74

	def test_max_hit(self):
		self.assertEqual(
			Melee().max_hit(100, self.r, Potions.ranging(self.r), Prayers.level2('ranged_strength'), Equipment.void_ranger()['ranged_strength'], 3, 1, 1),
			29
		)

	def test_attack_roll(self):
		self.assertEqual(
			Melee().max_attack_roll(115, self.r, Potions.ranging(self.r), Prayers.level2('ranged'), Equipment.void_ranger()['ranged'], 3, 1),
			#20_406  # from bitterkoekje but they floor after every operation.
			20_227
		)

