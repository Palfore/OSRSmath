"""	All these methods should ideally support:
		Negative Iterations: asking "how many turns ago" is possibly important for extensions to handling health regeneration.

	Otherwise, they should explicitly fail.

"""
from osrsmath.model.successful_hits import *
import unittest

class TestCrude(unittest.TestCase):
	h_0 = 100
	m = 10

	def test_0_hits_returns_initial_health(self):
		self.assertEqual(Crude().h(0, self.h_0, self.m), self.h_0)

	def test_1_hit_returns_m_2_less_health(self):
		self.assertEqual(Crude().h(1, self.h_0, self.m), self.h_0 - self.m/2)

	def test_kill_turns_gives_0_health(self):
		self.assertEqual(Crude().h(20, self.h_0, self.m), 0)

	def test_h_handles_fractions(self):
		self.assertAlmostEqual(Crude().h(12.43, self.h_0, self.m), 37.85)

	# def test_h_handles_negative_turns(self):
	# 	self.assertAlmostEqual(Crude().h(12.43, self.h_0, self.m), 37.85)


	def test_turns_to_initial_health_is_0(self):
		self.assertEqual(Crude().hinv(self.h_0, self.h_0, 10), 0)

	def test_turns_to_m_2_less_health_is_1(self):
		self.assertEqual(Crude().hinv(self.h_0 - self.m/2, self.h_0, 10), 1)

	# def test_hinv_handles_fractions(self):
	# 	self.assertEqual(Crude().hinv(2.354, self.h_0, 10), 0)

	# def test_hinv_handles_negative_turns(self):
	# 	self.assertEqual(Crude().hinv(2.354, self.h_0, 10), 0)


	def test_h_of_hinv_of_x_is_x(self):
		self.assertEqual(Crude().hinv(Crude().h(4, self.h_0, self.m), self.h_0, self.m), 4)

	def test_hinv_of_h_of_x_is_x(self):
		self.assertEqual(Crude().h(Crude().hinv(52, self.h_0, self.m), self.h_0, self.m), 52)

class BitterKoekje_Nukelawe(unittest.TestCase):
	h_0 = 100
	m = 10
	BN = BitterKoekje_Nukelawe

	def test_h_of_hinv_of_x_is_x(self):
		print(self.BN().hinv(0, self.h_0, self.m))
		print(self.BN().h(self.BN().hinv(0, self.h_0, self.m), self.h_0, self.m))
		self.assertAlmostEqual(self.BN().h(self.BN().hinv(0, self.h_0, self.m), self.h_0, self.m), 0)


		self.assertAlmostEqual(self.BN().h(self.BN().hinv(5, self.h_0, self.m), self.h_0, self.m), 5)


class Approximate(unittest.TestCase):
	pass

class Recursive(unittest.TestCase):
	pass

class MarkovChain(unittest.TestCase):
	pass