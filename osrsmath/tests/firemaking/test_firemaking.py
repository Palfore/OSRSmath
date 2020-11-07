from osrsmath.firemaking.wintertodt import *
import unittest

class TestWintertodt(unittest.TestCase):
	def test_roots_to_target(self):
		self.assertEqual(actions_to_target('root', 500), 50)
		self.assertEqual(actions_to_target('root', 4323), 433)

	def test_kindling_to_target(self):
		self.assertEqual(actions_to_target('kindling', 500), 20)
		self.assertEqual(actions_to_target('kindling', 4323), 173)

	def test_bonus_xp_is_100_times_level(self):
		self.assertEqual(bonus_experience(200_000), 5_600)
		for l in range(50, 99):
			with self.subTest(level=l):
				self.assertEqual(bonus_experience(experience(l)), l*100)

	def test_insuffient_points_gives_zero_crates(self):
		self.assertEqual(crates_per_kill(400), 0)

	def test_crates_per_kill(self):
		# https://oldschool.runescape.wiki/w/Supply_crate#Drop_mechanic
		self.assertEqual(crates_per_kill(500), 2)
		self.assertEqual(crates_per_kill(505), 2.01)
		self.assertEqual(crates_per_kill(750), 2.5)
		self.assertEqual(crates_per_kill(1005), 3.01)
		self.assertEqual(crates_per_kill(1500), 4)
	
	def test_excess_points_gives_maximum(self):
		self.assertEqual(crates_per_kill(10_000_000), 28)


class TestPolicies(unittest.TestCase):
	def setUp(self):
		self.fm = Firemaker(500_000, None)

	def test_roots_only(self):
		Policies.roots_only(self.fm, 2000)
		self.assertEqual(self.fm.xp, self.fm.E0 + 2000/10*66*3)

	def test_kindling_only(self):
		Policies.kindling_only(self.fm, 2000)
		self.assertEqual(self.fm.xp, self.fm.E0 + 2000/25*66*3.8)

	def test_kindling_till_x(self):
		Policies.kindling_till_x(self.fm, 2000, 610)
		self.assertEqual(self.fm.xp, self.fm.E0 + ceil((2000 - 25*ceil(610/25))/10)*66*3 + ceil(610/25)*66*3.8)

	def test_kindling_till_x_below_threshold(self):
		Policies.kindling_till_x(self.fm, 420, 610)
		self.assertEqual(self.fm.xp, self.fm.E0 + ceil((420 - 25*ceil(420/25))/10)*66*3 + ceil(420/25)*66*3.8)


class TestFiremaker(unittest.TestCase):
	def setUp(self):
		self.policy = Policies.roots_only
		self.fm = Firemaker(150_000, self.policy)

	def test_burning_single_root_gives_base_experience(self):
		self.assertEqual(self.fm.burn('root', 1), self.fm.E0 + 53*3.0)

	def test_burning_past_level_up(self):
		# 150_000 xp => 53 level
		# 150_872 xp => 54 level, requires 872 experience.
		# There are |`872 / (53*3)`| = 6 roots required to get to level 54.
		# after this, the experience gained is 54*3.
		# Test that 10 roots gives 53*3*6 + 54*3*4 experience.
		self.assertEqual(self.fm.burn('root', 10), self.fm.E0 + 53*3.0*6 + 54*3.0*4)

	def test_burning_no_roots_gives_starting_xp(self):
		self.assertEqual(self.fm.burn('root', 0), self.fm.E0)

	def test_insufficient_level_raises(self):
		self.assertRaises(ValueError, lambda:Firemaker(50_000))

	def test_kill_single_kill_no_level_up_or_bonus(self):
		fm = Firemaker(500_000, self.policy)  # Far from level up
		self.assertEqual(fm.kill(target_points=400, k=1), fm.E0 + 7_920)

	def test_kill_single_kill_no_level_up(self):
		fm = Firemaker(500_000, self.policy)  # Far from level up
		self.assertEqual(fm.kill(target_points=500, k=1), fm.E0 + 9_900 + 6_600)

	def test_kill_single_kill_level_up_no_bonus(self):
		fm = Firemaker(300_000, self.policy)  # close to level up
		# 2288 xp to level up. Level 60 gives 3*60=180 xp/root, so 13 roots are required
		# giving 2,340 experience. 400/10=40 roots need to be chopped total, leaving 27 left.
		# 27*3*61=4,941 experience from that. Total is then 2,340 + 4,941
		self.assertEqual(fm.kill(target_points=400, k=1), fm.E0 + 2_340 + 4_941)

	def test_kill_single_kill_level_up_and_bonus(self):
		fm = Firemaker(300_000, self.policy)  # close to level up
		# 2288 xp to level up. Level 60 gives 3*60=180 xp/root, so 13 roots are required
		# giving 2,340 experience. 600/10=60 roots need to be chopped total, leaving 47 left.
		# 47*3*61=4,941 experience from that. Bonus is 61*100=6_100. Total is then 2,340 + 4,941
		self.assertEqual(fm.kill(target_points=600, k=1), fm.E0 + 2_340 + 8_601 + 6_100)

class TestKills(unittest.TestCase):
	def test_upper_bound_on_kills(self):
		self.assertEqual(upper_bound_on_kills(743_042 - 65_123, 400), ceil((743_042 - 65_123) / ((400/25)*3.8*50)))
		self.assertEqual(upper_bound_on_kills(743_042 - 65_123, 610), ceil((743_042 - 65_123) / ((610/25)*3.8*50)))

	def test_kills_for_xp(self):
		# Work backwords: How much experience gained after num_kill kills at a given level?
		num_kills = 1000
		start_level = 50
		points_per_kill = 50
		fm = Firemaker(experience(start_level), Policies.roots_only)
		fm.kill(points_per_kill, num_kills)
		xp_gained = fm.xp - fm.E0
		self.assertEqual(kills_for_xp(fm.E0, fm.xp, points_per_kill, Policies.roots_only), num_kills)



	