from collections import defaultdict
from osrsmath.apps.optimize import get_sets, eval_set, load
from osrsmath.model.experience import combat_level
from osrsmath.model.boosts import BoostingSchemes, Prayers, Potions
from pprint import pprint
import matplotlib.pyplot as plt
import sys
import os

if __name__ == '__main__':
	player_stats, defenders, ignore, adjustments = config = load("settings.json")
	player_stats.update({
		'attack': 50,
		'strength': 50,
		'defence': 50,
	})
	player_stats.update({'cmb': combat_level(player_stats)})
	sets = get_sets(*config)

	graph = defaultdict(list)
	for s in sets:
		_, xp, stance = eval_set(
			player_stats, 'attack',
			lambda p: BoostingSchemes(p, Prayers.none).constant(Potions.overload),
			defenders, s
		)
		weapon = s['weapon'] if 'weapon' in s else s['2h']
		graph[weapon].append(xp)

	averages = {weapon: sum(xps)/len(xps) / 1_000 for weapon, xps in graph.items()}
	averages = {k: v for k, v in sorted(averages.items(), key=lambda x: x[1])}
	dmaxs = {weapon: max(xps) / 1_000 - averages[weapon] for weapon, xps in graph.items()}
	dmins = {weapon: averages[weapon] - min(xps) / 1_000 for weapon, xps in graph.items()}


	plt.bar(list(averages.keys()), list(averages.values()), yerr=[list(dmaxs.values()), list(dmins.values())], capsize=10)
	plt.xlabel('Weapon', fontsize=15)
	plt.ylabel('Average Exp Rate', fontsize=15)
	plt.gca().tick_params(axis='both', labelsize=12)
	plt.gca().set_xticklabels(list(averages.keys()), rotation=45, horizontalalignment ="right")
	plt.tight_layout()

	plt.ylim(min(list(averages.values())) - 5, max(list(averages.values())) + 5)
	if len(sys.argv) == 2 and sys.argv[1] == 'show':
		plt.show()
	else:
		file_name = 'weapon_comparison'
		plt.savefig(f"{file_name}.pdf")
		os.system(f"pdfcrop {file_name}.pdf")
		os.rename(f"{file_name}-crop.pdf", f"{file_name}.pdf")

