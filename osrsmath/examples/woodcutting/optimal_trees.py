from osrsmath.skills.woodcutting.entities import get_best_axe, trees
from osrsmath.skills.woodcutting.rates import get_xp_rate, get_optimal_training_order

if __name__ == '__main__':
	from pprint import pprint

	get_xp_rate('normal', get_best_axe(1), 1)
	
	pprint(get_optimal_training_order())
	# Normal: 1-14
	# Oak: 15-36
	# Teak: 37-69
	# mahogany 70-99

	
	# This should give 190/255 logs every 2.4 seconds
	# or (190/255)/2.4 logs every second
	# at 85 xp/log this gives 85*(190/255)/2.4 xp/second
	# print(get_xp_rate('teak', 'dragon', 99), 85*(190/255)/2.4 * 60*60)
	# print(get_xp_rate('teak', 'dragon', 1), 85*(60/255)/2.4 * 60*60)
	
	from mpl_toolkits.mplot3d import axes3d
	import matplotlib.pyplot as plt
	import numpy as np
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	def tree_at_level(level):
		for tree, data in trees.items():
			if data['level'] == level:
				return tree
		raise ValueError("No level found")

	@np.vectorize
	def f(x, y):
		return get_xp_rate(tree_at_level(y), get_best_axe(x), x) / 1_000


	x = list(range(1, 99+1))
	y = [data['level'] for tree, data in trees.items()]
	X, Y = np.meshgrid(x, y)
	Z = f(X, Y)
	ax.plot_wireframe(X, Y, Z)

	y = [35]
	X, Y = np.meshgrid(x, y)
	Z = f(X, Y) + 3
	ax.plot_wireframe(X, Y, Z, color='red', linewidth=5)

	y = [50, 60, 75, 90]
	X, Y = np.meshgrid(x, y)
	Z = f(X, Y) + 3
	ax.plot_wireframe(X, Y, Z, color='green', linewidth=5)
	
	ax.view_init(32, -146)
	plt.xlabel('Woodcutting Level')
	plt.ylabel('Tree Level')
	ax.set_zlabel('Experience Rate [k/h]')
	plt.show()
	# plt.savefig('experience.pdf')


	# for angle in range(0, 360):
	#     ax.view_init(30, angle)
	#     plt.draw()
	#     plt.pause(.001)

	# print("This is the teak xp rate at 99 using different axes")
	# for axe_name in axes:
	# 	print(axes[axe_name]['level'], get_xp_rate('teak', axe_name, 1))
	# print()

	# print("This is the teak xp rate using the best axe at all levels")
	# for level in range(1, 99+1):
	# 	print(level, get_xp_rate('teak', get_best_axe(level), level))
	# print()
