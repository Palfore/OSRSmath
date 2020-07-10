""" Tests h(n; h_0, M) and n(h; h_0, M) for the various models.

	The Recursive models have lots of exceptions due to how they treat things. They are also very
	difficult to compute by hand so testing them is difficult. So their testing is not complete.

	The Simulation model is not tested since it is stochastic, and the true values can only be known through simulation. """

from osrsmath.combat.successful_hits import *
import unittest
import numpy as np
import math

class Properties:
	@property
	def model(self):
		raise NotImplementedError

	@property
	def h_0(self):
		raise NotImplementedError

	@property
	def M(self):
		raise NotImplementedError

	@property
	def fractional_turns(self):
		raise NotImplementedError

	@property
	def fractional_health(self):
		raise NotImplementedError

	@property
	def negative_turns(self):
		raise NotImplementedError

	@property
	def negative_health(self):
		raise NotImplementedError


class TestHImplementation(Properties):
	@property
	def health_after_1_hit(self):
		raise NotImplementedError

	def test_0_hits_returns_initial_health(self):
		self.assertEqual(self.model().h(0, self.h_0, self.M), self.h_0)

	def test_1_hit_should_return_expected_value(self):
		self.assertEqual(self.model().h(1, self.h_0, self.M), self.health_after_1_hit)

	def test_fractional_turns_should_return_expected_value(self):
		self.assertAlmostEqual(self.model().h(self.fractional_turns, self.h_0, self.M), self.fractional_health)

	def test_negative_turns_should_return_expected_value(self):
		self.assertAlmostEqual(self.model().h(self.fractional_turns, self.h_0, self.M), self.fractional_health)


class TestHinvImplementation(Properties):
	@property
	def turns_to_1_less_health(self):
		raise NotImplementedError

	def test_initial_health_takes_zero_turns(self):
		self.assertEqual(self.model().hinv(self.h_0, self.h_0, self.M), 0)

	def test_1_less_health_should_return_expected_value(self):
		self.assertEqual(self.model().hinv(self.h_0 - 1, self.h_0, self.M), self.turns_to_1_less_health)

	def test_fractional_health_should_return_expected_value(self):
		self.assertAlmostEqual(self.model().hinv(self.fractional_health, self.h_0, self.M), self.fractional_turns)

	def test_negative_health_should_return_expected_value(self):
		self.assertAlmostEqual(self.model().hinv(self.fractional_health, self.h_0, self.M), self.fractional_turns)


class TestTurnsToKill(Properties):
	def test_max_hit_of_1_kills_in_two_times_initial_health_turns(self):
		# Let M = 1
		self.assertAlmostEqual(self.model().turns_to_kill(self.h_0, 1), 2*self.h_0)

	def test_health_of_1_dies_in_specific_turns(self):
		# Let h = 1
		# Chance of hitting at least 1 is M/(M+1). 1 over that is # turns
		self.assertAlmostEqual(self.model().turns_to_kill(1, self.M), (self.M+1)/self.M)


### Model Testing ###############################################################################
class TestCrude(TestTurnsToKill, TestHImplementation, TestHinvImplementation, unittest.TestCase):
	model = Crude
	h_0 = 100
	M = 10
	health_after_1_hit = h_0 - M / 2
	turns_to_1_less_health = 1 / (M / 2)
	fractional_turns = 3.543
	fractional_health = h_0 - fractional_turns * M / 2
	negative_turns = -2
	negative_health = h_0 + M

	def test_health_of_1_dies_in_specific_turns(self):
		# Override, since this model doesn't consider overkill.
		self.assertAlmostEqual(self.model().turns_to_kill(1, self.M), 2/self.M)

class TestAverage(TestTurnsToKill, unittest.TestCase):
	model = Average
	h_0 = 100
	M = 10

	def test_h_is_not_implemented(self):
		self.assertRaises(NotImplementedError, lambda: self.model().h(1, self.h_0, self.M))

	def test_hinv_does_not_support_arbitrary_h(self):
		self.assertRaises(AssertionError, lambda: self.model().hinv(1, self.h_0, self.M))

class TestRecursiveApproximation(unittest.TestCase):
	model = RecursiveApproximation
	h_0 = 10  # Overkill region
	M = 20

class TestRecursive(TestHImplementation, unittest.TestCase):
	# Doesn't inherit from TestTurnsToKill since its treatment is different
	model = Recursive
	h_0 = 11
	M = 20
	health_after_1_hit = 1/42 * (  ( 42*(M/42)**(2**(9/10)) )**2 + (42*(M/42)**(2**(9/10)) )**1  )

	def test_fractional_turns_should_return_expected_value(self):
		pass  # Ignore, very difficult to calculate by hand
	def test_negative_turns_should_return_expected_value(self):
		pass  # Ignore, very difficult to calculate by hand

	def test_0_hits_returns_initial_health(self):
		""" This model cannot output 0 due to its asymptotic nature. @see test_0_hits_does_not_return_initial_health """
		pass

	def test_0_hits_does_not_return_initial_health(self):
		self.assertNotAlmostEqual(self.model().h(0, self.h_0, self.M), self.h_0)

	def test_h_of_hinv_of_x_is_x(self):
		""" This seems to have no exceptions. """
		for i in np.arange(1, 50, 0.1):
			self.assertAlmostEqual(self.model().h(self.model().hinv(i, self.h_0, self.M), self.h_0, self.M), i)

	def test_hinv_of_h_of_x_is_x_in_particular_settings(self):
		""" @see test_hinv_of_h_has_exceptions """
		self.assertAlmostEqual(self.model().hinv(self.model().h(5, 11, self.M), 11, self.M), 5)

	def test_hinv_of_h_has_exceptions(self):
		""" Periodically (at multiples relating to h_0 and M), there are disagreements.
			They occur in bands (size 0.5) at integer multiples of M/2.
			These are not fully understood, but likely relate to the approximation. Most likely the approximation
			creates a multi-valued function, and the inversion finds an incorrect root.
			Maybe we can estimate the direction, like the desired root should always be above the crude starting estimate.
			Then we can perform a bounded search, eg: search within [Crude, inf]. """
		self.assertNotAlmostEqual(self.model().hinv(self.model().h(5, 10, self.M), 10, self.M), 5)

class TestMarkovChain(TestTurnsToKill, unittest.TestCase):
	model = MarkovChain
	h_0 = 100
	M = 20

	def test_h_is_not_implemented(self):
		self.assertRaises(NotImplementedError, lambda: self.model().h(1, self.h_0, self.M))

	def test_hinv_does_not_support_arbitrary_h(self):
		self.assertRaises(AssertionError, lambda: self.model().hinv(1, self.h_0, self.M))

	def test_only_first_term_included(self):
		# when (h - 1)/(M + 1) <= 1, like h_0=M, only the i=0 term is included
		self.assertAlmostEqual(self.model().turns_to_kill(self.M, self.M), ((self.M+1)/self.M)**self.M)

	def test_satisfies_recurrence_relations(self):
		with self.subTest("h > m + 1"):
			assert self.h_0 > (self.M + 1)
			self.assertAlmostEqual(self.model().turns_to_kill(self.h_0, self.M),
				(self.M + 1) / self.M * self.model().turns_to_kill(self.h_0 - 1, self.M)
				-1 / self.M * self.model().turns_to_kill(self.h_0 - self.M - 1, self.M)
			)

		with self.subTest("h <= m + 1"):
			h = 5
			assert h <= (self.M + 1)
			self.assertAlmostEqual(self.model().turns_to_kill(h, self.M),
				(self.M + 1) / self.M * self.model().turns_to_kill(h - 1, self.M)
			)

class TestMarkovChainApproximation(TestTurnsToKill, unittest.TestCase):
	model = MarkovChainApproximation
	h_0 = 100
	M = 10

	def test_h_is_not_implemented(self):
		self.assertRaises(NotImplementedError, lambda: self.model().h(1, self.h_0, self.M))

	def test_hinv_does_not_support_arbitrary_h(self):
		self.assertRaises(AssertionError, lambda: self.model().hinv(1, self.h_0, self.M))

	def test_health_of_1_dies_in_specific_turns(self):
		# Override, this is large h_0 approximation, so the standard doesn't hold here
		self.assertAlmostEqual(self.model().turns_to_kill(1, self.M), (2/3) * (1 + 2/self.M))