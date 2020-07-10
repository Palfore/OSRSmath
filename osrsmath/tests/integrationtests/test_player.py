from osrsmath.combat.player import *
from osrsmath.combat.monsters import *
from osrsmath.combat.boosts import *
from osrsmath.combat.experience import single_state_xp_rate, xp_rate, time_to_level
import unittest


class TestPlayer(unittest.TestCase):
	# https://www.osrsbox.com/blog/2019/01/22/calculating-melee-dps-in-osrs/#11-determine-effective-level
	# But differs slightly due to rounding choices

	# def test_single_opponent(self):
	# 	player = PlayerBuilder({
	# 		'attack': 97,
	# 		'strength': 99,
	# 	}).equip([
	# 		"Abyssal whip",
	# 		"Slayer helmet (i)",
	# 		"Bandos chestplate",
	# 		"Bandos tassets",
	# 		"Primordial boots",
	# 		"Holy Blessing",
	# 		"Barrows Gloves",
	# 		"Dragon Defender",
	# 		"Berserker Ring (i)",
	# 		"Amulet of torture",
	# 		"Fire Cape",
	# 	]).get()
	# 	player.combat_style = 'flick'
	# 	# player.print()

	# 	monster = Monster.from_name("Abyssal Demon")
	# 	M = player.get_max_hit(
	# 		Potions.super,
	# 		Prayers.piety,
	# 	)
	# 	A = player.get_attack_roll(
	# 		Potions.super,
	# 		Prayers.piety,
	# 	)
	# 	D = monster.get_defence_roll(
	# 		player.get_stances()[player.combat_style]['attack_type']
	# 	)
	# 	a = player.get_accuracy(A, D)

	# 	self.assertEqual(M, 54)
	# 	self.assertEqual(A, 34_600)
	# 	self.assertEqual(D, 12_096)
	# 	self.assertAlmostEqual(a, 0.8251784630502008)

	# def test_multiple_opponents(self):
	# 	opponents = {n: Monster.from_name(n) for n in [
	# 		"Trapped Soul", "Count Draynor", "Sand Snake", "King Roald", "The Kendal", "Tree spirit"
	# 	]}

	# 	player = PlayerBuilder({
	# 		'attack': 97,
	# 		'strength': 99,
	# 	}).equip([
	# 		"Abyssal whip",
	# 		"Slayer helmet (i)",
	# 		"Bandos chestplate",
	# 		"Bandos tassets",
	# 		"Primordial boots",
	# 		"Holy Blessing",
	# 		"Barrows Gloves",
	# 		"Dragon Defender",
	# 		"Berserker Ring (i)",
	# 		"Amulet of torture",
	# 		"Fire Cape",
	# 	]).get()
	# 	player.combat_style = 'flick'
	# 	# player.print()

	# 	M = player.get_max_hit(
	# 		Potions.super,
	# 		Prayers.piety,
	# 	)
	# 	A = player.get_attack_roll(
	# 		Potions.super,
	# 		Prayers.piety,
	# 	)
	# 	rate = single_state_xp_rate(
	# 		player.get_stances()[player.combat_style]['attack_type'],
	# 		M, A, player.get_stats()['attack_speed'], opponents)
	# 	self.assertAlmostEqual(rate, 114838.84962731639)

	# def test_multiple_states(self):
	# 	opponents = {n: Monster.from_name(n) for n in [
	# 		"Trapped Soul", "Count Draynor", "Sand Snake", "King Roald", "The Kendal", "Tree spirit"
	# 	]}

	# 	player = PlayerBuilder({
	# 		'attack': 97,
	# 		'strength': 99,
	# 		'defence': 1
	# 	}).equip([
	# 		"Abyssal whip",
	# 		"Slayer helmet (i)",
	# 		"Bandos chestplate",
	# 		"Bandos tassets",
	# 		"Primordial boots",
	# 		"Holy Blessing",
	# 		"Barrows Gloves",
	# 		"Dragon Defender",
	# 		"Berserker Ring (i)",
	# 		"Amulet of torture",
	# 		"Fire Cape",
	# 	]).get()
	# 	player.combat_style = 'flick'
	# 	# player.print()

	# 	boosts = BoostingSchemes(player, Prayers.piety).constant(Potions.overload)
	# 	xp = player.xp_rate(boosts, opponents)
	# 	t = player.time_to_level(boosts, opponents)
	# 	# print(xp, t)

	def test_multiple_states_ranged(self):
		# This should fail since there are no bolts
		opponents = {n: Monster.from_name(n) for n in [
			"Trapped Soul", "Count Draynor", "Sand Snake", "King Roald", "The Kendal", "Tree spirit"
		]}

		player = PlayerBuilder({
			'ranged': 83,
			'defence': 75
		}).equip([
			"Rune crossbow",
			# "Slayer helmet (i)",
			# "Bandos chestplate",
			# "Bandos tassets",
			# "Primordial boots",
			# "Holy Blessing",
			# "Barrows Gloves",
			# "Dragon Defender",
			# "Berserker Ring (i)",
			# "Amulet of torture",
			# "Fire Cape",
		]).get()
		player.combat_style = 'rapid'
		# player.print()

		boosts = BoostingSchemes(player, Prayers.level3).constant(Potions.overload)
		xp = player.xp_rate(boosts, opponents)
		t = player.time_to_level(boosts, opponents)
		print(xp, t)