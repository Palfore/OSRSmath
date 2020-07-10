import osrsmath.combat.successful_hits as successful_hits
from osrsmath.combat.rates import experience_per_hour
from osrsmath.combat.damage import accuracy
from math import floor

def combat_level(stats: dict, integer=True):
	required_stats = ('attack', 'strength', 'defence', 'hitpoints', 'prayer', 'ranged', 'magic')
	for s in required_stats:
		if s not in stats:
			raise ValueError(f"You must provide the {s} level to be able to calculate combat level.")
	base = 0.25 * (stats['defence'] + stats['hitpoints'] + floor(stats['prayer'] / 2))
	melee = 0.325 * (stats['attack'] + stats['strength'])
	ranged = 0.325 * floor(3*stats['ranged']/2)
	mage = 0.325 * floor(3*stats['magic']/2)
	level = base + max(melee, ranged, mage)
	return floor(level) if integer else level

def experience_required_to_level_up_to(level: int):
	""" Off by at most 1xp. """
	assert level >= 2, level
	x = level - 1
	return floor( x + 300 * 2**(x / 7) ) / 4

def single_state_xp_rate(attack_style, max_hit, max_attack_roll, attack_speed, defenders: dict, model='MarkovChain'):
	""" Returns the xp/h averaged across all defenders, given the attack is in a constant state. """
	average = 0
	for name, defender in defenders.items():
		D = defender.get_defence_roll(attack_style)
		a = accuracy(max_attack_roll, D)
		E = experience_per_hour(defender.levels['hitpoints'], max_hit, a, attack_speed, 4, getattr(successful_hits, model)())
		average += E
	average /= len(defenders)
	return average

def xp_rate(attack_type, attack_speed, states: list, defenders: dict, model='MarkovChain'):
	""" Returns the xp/h averaged across all defenders, given that the attacker is in a time-dependent state.
		This then performs that average across all states. """
	avg_xp = 0
	for M, A in states:
		avg_xp += single_state_xp_rate(
			attack_type, M, A, attack_speed, defenders, model
		)
	return avg_xp / len(states)

def time_to_level(current_level, experience_rate):
	""" get_time_to_level(player 'attack', BoostingSchemes(player).overload(), opponents) """
	return experience_required_to_level_up_to(current_level + 1) / experience_rate

if __name__ == '__main__':
	from osrsmath.combat.player import PlayerBuilder
	from osrsmath.combat.boosts import BoostingSchemes
	from osrsmath.combat.monsters import Monster

	player = PlayerBuilder({"attack": 70, "strength": 90, "defence": 70}).equip([
		"Dragon Scimitar",
		"Dharok's helm",
		"Dharok's platebody",
		"Dharok's platelegs",
		"Dragon Boots",
		"Holy Blessing",
		"Barrows Gloves",
		"Dragon Defender",
		"Berserker Ring (i)",
		"Amulet of Fury",
		"Fire Cape",
	]).get()
	player.print()
	player.combat_style = 'chop'
	print()

	xp_h = time_dependent_model_xp(BoostingSchemes(player).super_combat_when_skill_under("attack", 5), {
			'Count Draynor': Monster.from_id(6332),
	})
	print(xp_h)
