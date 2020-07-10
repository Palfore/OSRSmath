"""	All these methods should ideally support:
		Negative Iterations: asking "how many turns ago" is possibly important for extensions to handling health regeneration.

	Otherwise, they should explicitly fail.

"""
from osrsmath.apps.optimize import *
from osrsmath.combat.player import get_equipment_data, get_equipment_by_name
import unittest

EQ = get_equipment_data()

class TestIsOffensivelyEqual(unittest.TestCase):
	def test_different_charged_jewlery_are_equal(self):
		self.assertTrue(is_offensively_equal(
			get_equipment_by_name("Amulet of glory(3)", 'neck', EQ),
			get_equipment_by_name("Amulet of glory(2)", 'neck', EQ)
		))

	def test_same_armour_is_the_same(self):
		self.assertTrue(is_offensively_equal(
			get_equipment_by_name("Amulet of glory(2)", 'neck', EQ),
			get_equipment_by_name("Amulet of glory(2)", 'neck', EQ)
		))

	def test_different_armour_is_false(self):
		self.assertFalse(is_offensively_equal(
			get_equipment_by_name("Amulet of fury", 'neck', EQ),
			get_equipment_by_name("Amulet of glory(2)", 'neck', EQ)
		))

class TestIsOneSimplyBetter(unittest.TestCase):
	def test_different_charged_jewlery_are_equal(self):
		self.assertFalse(is_one_simply_better(
			get_equipment_by_name("Amulet of glory(3)", 'neck', EQ),
			get_equipment_by_name("Amulet of glory(2)", 'neck', EQ)
		))

	def test_same_armour_is_the_same(self):
		self.assertFalse(is_one_simply_better(
			get_equipment_by_name("Amulet of glory(2)", 'neck', EQ),
			get_equipment_by_name("Amulet of glory(2)", 'neck', EQ)
		))

	def test_different_armour_is_false(self):
		self.assertEqual(is_one_simply_better(
			get_equipment_by_name("Amulet of fury", 'neck', EQ),
			get_equipment_by_name("Amulet of glory(2)", 'neck', EQ)
		), get_equipment_by_name("Amulet of fury", 'neck', EQ))






