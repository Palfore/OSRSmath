if __name__ == '__main__':
	from model.monsters import Monster, get_monster_data
	from model.player import Player, get_equipment_data
	from model.rates import experience_per_hour
	from model.successful_hits import *
	from pprint import pprint

	equipment_data = get_equipment_data()
	monster_data = get_monster_data()

	attacker = Player({'attack': 70, 'strength': 85, 'defence': 70, 'prayer': 56, 'hitpoints': 79, 'magic': 71, 'ranged': 70})
	attacker.equip_by_name("Dragon Scimitar")
	attacker.equip_by_name("Dharok's helm")
	attacker.equip_by_name("Dharok's platebody")
	attacker.equip_by_name("Dharok's platelegs")
	attacker.equip_by_name("Dragon Boots")
	attacker.equip_by_name("Holy Blessing")
	attacker.equip_by_name("Barrows Gloves")
	attacker.equip_by_name("Dragon Defender")
	attacker.equip_by_name("Berserker Ring (i)")
	attacker.equip_by_name("Amulet of Fury")
	attacker.equip_by_name("Fire Cape")
	attacker.combat_style = 'slash'

	defender = Monster.from_name("Count Draynor (hard)")

	stats = attacker.get_stats()
	m = attacker.get_max_hit(0, 1, 1, 1)
	A = attacker.get_attack_roll(0, 1, 1, 1)
	D = defender.get_defence_roll(attacker.get_stances()[attacker.combat_style]['attack_type'], 0, 1, 1, 1)
	a = defender.get_accuracy(A, D)
	E = experience_per_hour(defender.levels['hitpoints'], m, a, 1 / stats['attack_speed'], 4, BitterKoekje_Nukelawe())
