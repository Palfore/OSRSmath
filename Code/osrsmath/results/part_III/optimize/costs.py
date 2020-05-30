# from jsoncomment import JsonComment
# from osrsmath.apps.optimize import get_sets, get_best_set
# from osrsmath.model.player import get_equipment_data
# from osrsmath.model.experience import combat_level
# from osrsmath.model.monsters import Monster
# from osrsmath.model.boosts import BoostingSchemes
# from pprint import pprint
# import sys
# import os

# costs = {  # Manually obtained on 2020-03-24, from wiki
# 	'Gadderhammer': 1_300,
# 	'Spiked manacles': 1_170_000,
# 	'Regen bracelet': 2_279_005,
# 	'Fremennik kilk': 5_332_258,
# 	'Amulet of torture': 17_054_112,
# 	'Brimstone ring': 4_106_804,
# 	'Warrior ring (i)': 42_983,
# 	'Black scimitar': 1_435,
# 	'Mithril scimitar': 392,
# 	'Adamant scimitar': 1_338,
# 	'Rune Gloves': 6_500,
# 	'Brine sabre': 149_403,
# 	'Barrows gloves': 100_000,
# 	'Berserker helm': 44_264,
# 	'Granite hammer': 831_247,
# 	'Obsidian platebody': 1_017_874,
# 	'Dragon Boots': 302_179,
# 	'Warrior helm': 41_863,
# 	'Obsidian platelegs': 821_706,
# 	'Berserker ring (i)': 2_804_443,
# 	'Dragon scimitar': 59_568,
# 	'Bandos chestplate': 20_353_605,
# 	'Neitiznot faceguard': 27_312_230 + 51_563,
# 	'Bandos tassets': 29_438_824,
# 	'Avernic defender': 83_636_792,
# 	'Abyssal whip': 2_541_568,
# 	'Primordial boots': 32_007_307,
# 	'Ferocious gloves': 6_202_804,
# 	'Blade of saeldor': 137_764_117,
# }

# if __name__ == '__main__':
# 	# Retrieve Data
# 	EQD = get_equipment_data()
# 	parser = JsonComment()
# 	data = parser.loadf("settings.json")

# 	player_stats = data['player_stats']
# 	defenders = {}
# 	for name, (search_type, value) in data['defenders'].items():
# 		if search_type == 'id':
# 			defenders[name] = Monster.from_id(value)
# 		elif search_type == 'name':
# 			defenders[name] = Monster.from_name(value)
# 		else:
# 			raise ValueError(f'The search type must be either "id" or "name", not {search_type}')
# 	ignore = data['ignore']
# 	adjustments = data['adjustments']

# 	graph = []
# 	for i in [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99]:
# 		player_stats.update({
# 			'attack': i,
# 			'strength': i,
# 			'defence': i,
# 		})
# 		player_stats.update({'cmb': combat_level(player_stats)})
# 		sets = get_sets(data['training_skill'], defenders, player_stats, ignore, adjustments, EQD)
# 		sets = [{ slot: eq for slot, eq in s if eq is not None} for s in sets]
# 		print(f"There are {len(sets)} sets.")
# 		s, xp, stance = best = get_best_set(player_stats, 'attack', lambda p: BoostingSchemes(p).overload(), defenders, sets)

# 		cost = sum(costs.get(e, 0) for s, e in s.items()) / 1_000_000
# 		graph.append({'level': i, 'xp': xp, 'cost': cost, 'xp/cost': xp/cost})
# 		pprint(s)
# 		print(i, xp, cost)

# 	import matplotlib.pyplot as plt
# 	plt.plot([c['level'] for c in graph], [c['xp/cost'] for c in graph], linewidth=5)
# 	plt.xlabel('Level', fontsize=15)
# 	plt.ylabel('Gold Efficiency [Exp Rate / Million GP]', fontsize=15)
# 	plt.gca().tick_params(axis='both', labelsize=12)
# 	plt.tight_layout()

# 	if len(sys.argv) == 2 and sys.argv[1] == 'show':
# 		plt.show()
# 	else:
# 		file_name = 'gold_efficiency'
# 		plt.savefig(f"{file_name}.pdf")
# 		os.system(f"pdfcrop {file_name}.pdf")
# 		os.rename(f"{file_name}-crop.pdf", f"{file_name}.pdf")

