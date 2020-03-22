import osrsmath.model.successful_hits as successful_hits
from osrsmath.model.rates import experience_per_hour
from osrsmath.model.player import Player
from math import floor

def experience_till_next_level(level):
	assert level >= 2, level
	x = level - 1
	return floor( x + 300 * 2**(x / 7) ) / 4

def level_by_experience(experience):
	raise NotImplementedError("In Development")
	assert 0 <= experience <= 200_000_000

	MAX_LEVEL_DUE_TO_EXPERIENCE_CAP = 126
	xp = 0
	for level in range(1, MAX_LEVEL_DUE_TO_EXPERIENCE_CAP+1):
		xp += experience_till_next_level(level)
		if xp >= experience:
			return level
	assert False, f"Calculation Error"

def average_xp(attacker, max_hit, max_attack_roll, attack_speed, defenders: dict, model='Recursive'):
	""" Returns the xp/h averaged across all defenders, given the attack is in a constant state. """
	average = 0
	attackers_attack_type = attacker.get_stances()[attacker.combat_style]['attack_type']
	for name, defender in defenders.items():
		D = defender.get_defence_roll(attackers_attack_type, 0, 1, 1, 1)
		a = Player.get_accuracy(max_attack_roll, D)
		E = experience_per_hour(defender.levels['hitpoints'], max_hit, a, 1 / attack_speed, 4, getattr(successful_hits, model)())
		average += E
	average /= len(defenders)
	return average

def time_dependent_model_xp(states: list, defenders: dict, model='Recursive'):
	""" Returns the xp/h averaged across all defenders, given that the attacker is in a time-dependent state.
		This then performs that average across all states. """
	xp_h = 0
	for attacker in states:
		max_hit = attacker.get_max_hit(0, 1, 1, 1)
		A = attacker.get_attack_roll(0, 1, 1, 1)
		xp_h += average_xp(attacker, max_hit, A, attacker.get_stats()['attack_speed'], defenders, model)
	return xp_h / len(states)

def get_time_to_level(player, training_skill, states, defenders):
	""" get_time_to_level(player 'attack', BoostingSchemes(player).overload(), opponents) """
	return experience_till_next_level(player.levels[training_skill] + 1) / time_dependent_model_xp(states, defenders, 'Recursive')

if __name__ == '__main__':
	from osrsmath.model.player import PlayerBuilder
	from osrsmath.model.boosts import BoostingSchemes
	from osrsmath.model.monsters import Monster

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