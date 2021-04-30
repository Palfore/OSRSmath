from osrsmath.skills.mining.motherload_mine import Miner, base_xp, PROSPECTOR
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from pprint import pprint
import itertools

def get_optimal_kit(paydirt_xp):
	experience = {}
	for item1, item2, item3, item4 in itertools.permutations(PROSPECTOR):
		miner = Miner(xp_per_paydirt=paydirt_xp)
		miner.obtain(item1)
		miner.obtain(item2)
		miner.obtain(item3)
		miner.obtain(item4)
		experience[miner.kit()] = miner.experience_gained - base_xp(paydirt_xp)
	return {''.join(l[0] for l in k): v for k, v in sorted(experience.items(), key=lambda x: x[1])}

if __name__ == '__main__':
	file_prefix='varying_paydirt'
	data = {}
	for paydirt_xp in range(2, 10_000):
		x = list(reversed(list(enumerate(reversed(get_optimal_kit(paydirt_xp).keys()), 1))))
		data[paydirt_xp] = {y: i for i, y in x}

	plot = {}
	for key in data[60]:
		plot[key] = ((
			list(data.keys()), [
			datum[key] for paydirt_xp, datum in data.items()
		]))

	for x_max in [100, 1_000, 10_000]:
		fig, ax = plt.subplots()
		fig.set_size_inches(16, 8)
		for i, (key, (x, y)) in enumerate(plot.items()):
			plt.plot(x[:x_max], y[:x_max], label=key)
		plt.plot([60, 60], [0, 25], color='black')
		plt.ylabel('Ranking', fontsize=18)
		plt.xlabel('Paydirt Experience', fontsize=18)
		ax.tick_params(axis='both', which='major', labelsize=16)
		ax.tick_params(axis='both', which='minor', labelsize=10)
		plt.legend(loc='right')
		plt.savefig(f'{file_prefix}.{x_max}.pdf')
		plt.savefig(f'{file_prefix}.{x_max}.png')


					
