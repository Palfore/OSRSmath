if __name__ == '__main__':
	from osrsmath.skills.firemaking.wintertodt import *
	import matplotlib.pyplot as plt
	import matplotlib as mpl
	import time
	
	plt.style.use('seaborn-poster')
	mpl.rcParams['xtick.labelsize'] = 20
	mpl.rcParams['ytick.labelsize'] = 20
	fontsize = 30
	legendsize = 20

	start = time.time()
	e50, e99 = experience(50), experience(99)

	## Plotting kills vs points for 50-99 fm, for different policies
	policies = {
		'Roots': [],
		'Kindling': [],
		'Kindling Till Bonus': [],
	}

	# point_list = list(range(25, 2000+25, 1))
	# for points in point_list:
	# 	policies['Roots'].append((points, kills_for_xp(e50, e99, points, Policies.roots_only)))
	# 	policies['Kindling'].append((points, kills_for_xp(e50, e99, points, Policies.kindling_only)))
	# 	policies['Kindling Till Bonus'].append((points, kills_for_xp(e50, e99, points, Policies.kindling_till_bonus)))
	# 	print(points)

	# for policy, data in policies.items():
	# 	plt.plot(*list(zip(*data)), label=f"Policy={policy}", linewidth=8)
	# plt.ylabel('Kills Required for 50-99 fm', fontsize=fontsize)
	# plt.xlabel('Points per Kill', fontsize=fontsize)
	# plt.xlim(0, 2000)
	# plt.ylim(0, 3000)
	# plt.legend(loc='upper right', prop={'size': 1.2*legendsize}, framealpha=0)
	# # plt.grid('on')
	# print(f'Evaluated in {time.time() - start}.')
	# plt.savefig('policies.pdf', transparent=True)
	# plt.show()


	## Plotting grand exchange value from 50-99 firemaking, for different base levels & points per game,
	# for a fixed policy.
	# Values obtained from https://oldschool.runescape.wiki/w/Calculator:Wintertodt_supply_crate on 2020-11-04
	# for 500 points. So, each value is later divided by two since 500 points the value for 2 rolls.
	roll_values = {
		( 1,  500):  6_799.85,
		( 1,  750):  8_308.68,
		( 1, 1000):  9_817.50,
		# ( 1, 5000): 33_958.73,
		(40,  500): 12_371.24,
		(40,  750): 15_272.91,
		(40, 1000): 18_174.59,
		# (40, 5000): 64_601.38,
		(75,  500): 16_543.89,
		(75,  750): 20_488.73,
		(75, 1000): 24_433.57,
		# (75, 5000): 87_550.98,
		(99,  500): 17_220.78,
		(99,  750): 21_334.85,
		(99, 1000): 25_448.91,
		# (99, 5000): 91_273.88,
	}
	roll_values = {k: v/2 for k, v in roll_values.items()}
	vs_points = {}
	vs_base = {}
	for (base, points), value in roll_values.items():
		kills_required = kills_for_xp(experience(50), experience(99), points, Policies.roots_only)
		# kills_required = kills_for_xp(experience(50), experience(99), points, Policies.kindling_only)
		total = value*rolls_per_kill(points)*kills_required

		vs_points.setdefault(base, []).append((points, total/1_000_000))
		vs_base.setdefault(points, []).append((base, total/1_000_000))
	
	fig, (ax1, ax2) = plt.subplots(2, 1)
	for base in vs_points:
		ax1.plot(*list(zip(*vs_points[base])), label=f"Base={base}", linewidth=8)
		ax1.scatter(*list(zip(*vs_points[base])), s=300)
	ax1.set_ylabel('Profit [Millions]', fontsize=fontsize)
	ax1.set_xlabel('Points per kill', fontsize=fontsize)
	# ax1.set_xlim(450, 1050)
	ax1.set_ylim(top=20)
	ax1.legend(loc='upper left', framealpha=0, prop={'size': legendsize}, ncol=4)
	# ax1.grid('on')

	for points in vs_base:
		ax2.plot(*list(zip(*vs_base[points])), label=f"Points={points}", linewidth=8)
		ax2.scatter(*list(zip(*vs_base[points])), s=300)
	ax2.set_ylabel('Profit [Millions]', fontsize=fontsize)
	ax2.set_xlabel('Base level', fontsize=fontsize)
	ax2.set_ylim(top=20)
	ax2.legend(loc='upper left', framealpha=0, prop={'size': legendsize}, ncol=3)
	# ax2.grid('on')

	fig.tight_layout()
	plt.savefig('profit.pdf', transparent=True)
	# plt.show()
