from osrsmath.results.part_II.colors import colors
from osrsmath.model.successful_hits import *
from osrsmath.results.part_II.generate_simulation import load_dataset
from pprint import pprint
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import osrsmath.config as config

if __name__ == '__main__':
	showing = len(sys.argv) >= 2 and sys.argv[1] == 'show'
	fig, ax = config.get_figure(38, 17, scale=3 if showing else 10)

	m_min, m_max = (1, 110)
	h_min, h_max = (1, 255)
	max_hits = np.array(range(m_min, m_max+1))
	healths = np.array(range(h_min, h_max+1))
	Ms, Hs = np.meshgrid(max_hits, healths)
	sim = load_dataset(N=100_000)

	def plot_error(label, inverse):
		""" inverse: hinv(h, m) """
		def err(a, b):
			# return abs(a - b)
			return abs(1 - a /b)*100
		print(label)
		Z = np.array([np.array([err(inverse(h, m), sim[str(h)][str(m)]) for m in max_hits]) for h in healths])
		surf = ax.plot_wireframe(Ms, Hs, Z, color=colors[label], linewidth=2.3, label=f"{label}")
		return {label: (np.average(Z), np.std(Z), np.max(Z), np.min(Z))}

	values = {}
	for method in Model.__subclasses__():
		if method.__name__ == 'Simulation':
			continue
		values.update(plot_error(method.__name__, lambda h, m: method().turns_to_kill(h, m)))

	print(R"\begin{table}[h]")
	print('\t' + R"\centering")
	print('\t' + R"\begin{tabular}{ l | c c c c }")
	print('\t\t' + R"Model & Average & Standard Deviation & Maximum & Minimum \\")
	print('\t\t' + R"\hline\hline")
	for label, (avg, stdd, M, m) in values.items():
		print('\t\t' Rf'{label} & {avg:.2f} & {stdd:.2f} & {M:.2f} & {m:.2e} \\')
	print('\t' + R"\end{tabular}")
	print('\t' + R"\caption{Error statistics for various models.}")
	print('\t' + R"\label{table:model_comp_stats}")
	print(R"\end{table}")
	# exit()

	ax.tick_params(axis='z', labelsize=12)
	ax.tick_params(axis='y', labelsize=12)
	ax.tick_params(axis='x', labelsize=12)
	ax.set_zlabel("Percent Error", fontsize=16, labelpad=20)
	plt.xlabel("Max Hit", fontsize=16, labelpad=20)
	plt.ylabel("Initial Health", fontsize=16, labelpad=20)
	leg = plt.legend(loc=(0.6, 0.6), fancybox=True, fontsize=16, markerscale=5)
	for legobj in leg.legendHandles:
		legobj.set_linewidth(4)


	if showing:
		plt.show()
	else:
		from pathlib import Path
		file_name = str(Path(__file__).parent/'errors')
		plt.savefig(f"{file_name}.png")
		os.system(f"convert {file_name}.png -trim {file_name}.png")
		# plt.savefig(f"{file_name}.pdf")
		# os.system(f"pdfcrop {file_name}.pdf")
		# os.rename(f"{file_name}-crop.pdf", f"{file_name}.pdf")

