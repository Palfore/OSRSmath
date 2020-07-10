from osrsmath.combat.hits import *
import unittest

class FakeModel:
	def h(self, n, h_0, M):
		""" Captures these properties:
				h decreases as n increases,
				h increases as h_0 increases,
				h increases as M increases,
				h is inverse of hinv """
		return h_0 * M / n - 1

	def hinv(self, h, h_0, M):
		""" Captures these properties:
				n increases as (h_0 - h) increases,
				n decreases as M increases,
				hinv is inverse of h """
		return M * h_0 / ( h + 1 )  # +1 to avoid division by 0

	def turns_to_kill(self, h_0, M):
		return self.hinv(0, h_0, M)


class TestAttacksToKillComparisons(unittest.TestCase):
	a2k = lambda self, a: attacks_to_kill(100, 30, a, FakeModel())
	higher = 0.8
	lower = 0.65

	def setUp(self):
		assert self.higher > self.lower

	def test_accuracy_is_multiplicative(self):
		self.assertAlmostEqual( self.a2k(self.higher) / self.a2k(self.lower), self.lower / self.higher)

	def test_accuracy_decreases_turns_to_kill(self):
		self.assertLess(self.a2k(self.higher), self.a2k(self.lower))


class TestAttacksUntilHealthComparisons(unittest.TestCase):
	a2h = lambda self, a: attacks_until_health(10, 100, 30, a, FakeModel())
	higher = 0.8
	lower = 0.65

	def setUp(self):
		assert self.higher > self.lower

	def test_accuracy_is_multiplicative(self):
		self.assertAlmostEqual( self.a2h(self.higher) / self.a2h(self.lower), self.lower / self.higher)

	def test_accuracy_decreases_turns_to_kill(self):
		self.assertLess(self.a2h(self.higher), self.a2h(self.lower))


class TestHealthAfterAttack(unittest.TestCase):
	haa = lambda self, a: health_after_attacks(10, 100, 30, a, FakeModel())
	higher = 0.8
	lower = 0.65

	def setUp(self):
		assert self.higher > self.lower

	def test_accuracy_decreases_health_after_attacks(self):
		self.assertLess(self.haa(self.higher), self.haa(self.lower))


class TestInverses(unittest.TestCase):
	haa = lambda self, n, a: health_after_attacks(n, 100, 30, a, FakeModel())
	a2h = lambda self, h, a: attacks_until_health(h, 100, 30, a, FakeModel())

	def test_health_after_attacks_is_inverse_of_attack_until_health(self):
		self.assertEqual(self.haa(self.a2h(5, 0.8), 0.8), 5)

	def test_attack_until_health_is_inverse_of_health_after_attacks(self):
		self.assertEqual(self.a2h(self.haa(5, 0.8), 0.8), 5)

