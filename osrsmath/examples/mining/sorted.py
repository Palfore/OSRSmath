from osrsmath.skills.mining.motherload_mine import Miner, base_xp, PROSPECTOR
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from pprint import pprint
import itertools

def normalize(dic):
	m, M = min(dic.values()), max(dic.values())
	return {k: round((v - m) / (M - m), 12) for k, v in dic.items()}

if __name__ == '__main__':
	file_name='sorted.pdf'
	experience = {}
	for item1, item2, item3, item4 in itertools.permutations(PROSPECTOR):
		miner = Miner()
		miner.obtain(item1)
		miner.obtain(item2)
		miner.obtain(item3)
		miner.obtain(item4)
		experience[miner.kit()] = miner.experience_gained - base_xp()
	m, M = min(experience.items(), key=lambda x: x[1])[1], max(experience.items(), key=lambda x: x[1])[1]
	sort = {''.join(l[0] for l in k): v for k, v in sorted(experience.items(), key=lambda x: x[1])}
	x = list(range(len(sort)))

	fig, ax = plt.subplots()
	fig.set_size_inches(16, 8)
	plt.ylim((m - 100, M + 100))
	plt.bar(x, sort.values())
	plt.xticks(x, sort.keys())
	plt.ylabel('Bonus Experience')
	plt.xlabel('Order Obtained')
	plt.legend(handles=[
		mpatches.Patch(label='J: Jacket'),
		mpatches.Patch(label='L: Legs'),
		mpatches.Patch(label='H: Helmet'),
		mpatches.Patch(label='B: Boots'),
	])
	# plt.show()
	plt.savefig(file_name)


					
