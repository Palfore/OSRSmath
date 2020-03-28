from osrsmath.model.damage import *
from osrsmath.model.boosts import *
import unittest

class TestMelee(unittest.TestCase):
	# https://www.osrsbox.com/blog/2019/01/22/calculating-melee-dps-in-osrs/

	a, s = 97, 99

	def test_max_hit(self):
		self.assertEqual(
			Melee().max_hit(133, self.s, Potions.super(self.s), Prayers.piety('strength'), Equipment.black_mask('strength'), 0, 1, 1),
			54
		)

	def test_attack_roll(self):
		self.assertEqual(
			Melee().max_attack_roll(136, self.a, Potions.super(self.a), Prayers.piety('attack'), 1, 3, Equipment.black_mask('attack')),
			35_000  # Not sure why black_mask is multiplier here, but other for strength?
		)

	def test_defence_roll(self):
		self.assertEqual(
			Melee().max_defence_roll(20, 135, 0, 1, 1, 1, 1),
			12_096
		)

	def test_accuracy(self):
		self.assertAlmostEqual(Melee.accuracy(35_000, 12_096), 0.82717636639)
