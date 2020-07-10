from osrsmath.combat.rates import *
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


class TestHealthAtTime(unittest.TestCase):
	hat = lambda self, T_A: health_after_time(5, 100, 30, 0.8, T_A, FakeModel())
	faster = 2.4
	slower = 3.0

	def setUp(self):
		assert self.faster < self.slower
		assert (1/self.faster) > (1/self.slower)

	def test_attack_period_decreases_health(self):
		self.assertLess(self.hat(self.faster), self.hat(self.slower))


class TestTimeUntilHealth(unittest.TestCase):
	tuh = lambda self, T_A: time_until_health(5, 100, 30, 0.8, T_A, FakeModel())
	faster = 2.4
	slower = 3.0

	def setUp(self):
		assert self.faster < self.slower
		assert (1/self.faster) > (1/self.slower)

	def test_attack_period_decreases_time(self):
		self.assertLess(self.tuh(self.faster), self.tuh(self.slower))

	def test_attack_period_is_multiplicative(self):
		self.assertAlmostEqual( self.tuh(self.faster) / self.tuh(self.slower), self.faster /  self.slower)


class TestTimeToKill(unittest.TestCase):
	ttk = lambda self, T_A: time_to_kill(100, 30, 0.8, T_A, FakeModel())
	faster = 2.4
	slower = 3.0

	def setUp(self):
		assert self.faster < self.slower
		assert (1/self.faster) > (1/self.slower)

	def test_attack_period_decreases_time(self):
		self.assertLess(self.ttk(self.faster), self.ttk(self.slower))

	def test_attack_period_is_multiplicative(self):
		self.assertAlmostEqual( self.ttk(self.faster) / self.ttk(self.slower), self.faster /  self.slower)


class TestExperiencePerHour(unittest.TestCase):
	xph = lambda self, T_A, e: experience_per_hour(100, 30, 0.8, T_A, e, FakeModel())
	faster = 2.4
	slower = 3.0
	more = 4.2
	less = 4.0

	def setUp(self):
		assert self.faster < self.slower
		assert (1/self.faster) > (1/self.slower)

	def test_attack_period_decreases_xp_rate(self):
		self.assertLess(self.xph(self.slower, self.less), self.xph(self.faster, self.less))

	def test_attack_period_is_multiplicative(self):
		self.assertAlmostEqual( self.xph(self.faster, self.less) / self.xph(self.slower, self.less), self.slower /  self.faster)

	def test_xp_multiplier_increases_xp_rate(self):
		self.assertGreater(self.xph(self.slower, self.more), self.xph(self.slower, self.less))

	def test_xp_multiplier_is_multiplicative(self):
		self.assertAlmostEqual( self.xph(self.slower, self.more) / self.xph(self.slower, self.less), self.more /  self.less)


class TestTimeUntilExperience(unittest.TestCase):
	huxp = lambda self, E: hours_until_experience(E, 100, 30, 0.8, 0.6, 4, FakeModel())
	more = 12_543
	less = 5_523

	def setUp(self):
		assert self.more > self.less

	def test_desired_experience_increases_time(self):
		self.assertGreater(self.huxp(self.more), self.huxp(self.less))

	def test_attack_period_is_multiplicative(self):
		self.assertAlmostEqual( self.huxp(self.more) / self.huxp(self.less), self.more /  self.less)
