from osrsmath.general.skills import *
import unittest

class TestExperience(unittest.TestCase):
	def test_experience_for_levels_below_1_raises(self):
		self.assertRaises(ValueError, lambda:experience(0))
		self.assertRaises(ValueError, lambda:experience(-3))

	def test_experience_for_levels_above_level_cap_with_no_flag_raises(self):
		self.assertRaises(ValueError, lambda:experience(100, virtual_levels=False))
		self.assertRaises(ValueError, lambda:experience(112, virtual_levels=False))

	def test_experience_for_levels_above_virtual_cap_raises(self):
		self.assertRaises(ValueError, lambda:experience(127))
		self.assertRaises(ValueError, lambda:experience(140))

	def test_experience_for_levels_below_level_cap(self):
		self.assertEqual(experience(85), 3_258_594)
		self.assertEqual(experience(34), 20_224)

	def test_experience_for_levels_above_virtual_cap_with_flag(self):
		self.assertEqual(experience(100, virtual_levels=True), 14_391_160)
		self.assertEqual(experience(112, virtual_levels=True), 47_221_641)


class TestLevel(unittest.TestCase):
	def test_experience_below_zero_raises(self):
		self.assertRaises(ValueError, lambda:level(-1))

	def test_experience_of_zero_is_lowest_level(self):
		self.assertEqual(level(0), 1)

	def test_experience_above_level_cap_returns_max_level_without_flag(self):
		self.assertEqual(level(14_000_000, virtual_levels=False), 99)
		self.assertEqual(level(200_000_000, virtual_levels=False), 99)

	def test_experience_above_level_cap_with_flag(self):
		self.assertEqual(level(14_000_000, virtual_levels=True), 99)
		self.assertEqual(level(112_000_000, virtual_levels=True), 120)
		self.assertEqual(level(200_000_000, virtual_levels=True), 126)

	def test_experience_above_maximum_experience_raises(self):
		self.assertRaises(ValueError, lambda:level(200_000_001))		
		self.assertRaises(ValueError, lambda:level(252_532_523))

	def test_experience_within_bounds(self):
		self.assertEqual(level(40_000), 40)
		self.assertEqual(level(700_000), 69)
		self.assertEqual(level(9_000_000), 95)

	def test_invertability(self):
		small_experience = 1
		for l in range(1, 99+1):
			with self.subTest(level=l):
				self.assertEqual(level(experience(l)), l)

	def test_experience_just_over_level_same_level(self):
		small_experience = 1
		for l in range(1, 99+1):
			with self.subTest(level=l):
				self.assertEqual(level(experience(l) + small_experience), l)

	def test_experience_just_under_level_is_previous_level(self):
		small_experience = 1
		for l in range(2, 99+1):
			with self.subTest(level=l):
				if l == 1:
					self.assertRaises(ValueError, lambda:level(experience(l) - small_experience))
				else:
					self.assertEqual(level(experience(l) - small_experience), l - 1)
