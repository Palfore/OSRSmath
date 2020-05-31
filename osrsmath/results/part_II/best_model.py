from osrsmath.results.part_II.colors import colors
from osrsmath.results.part_II.generate_simulation import load_dataset
import osrsmath.model.successful_hits as sh

import matplotlib as mpl
import matplotlib.colors as clrs
import matplotlib.pyplot as plt
import numpy as np
import operator
import sys
import inspect
import os

def draw(ax, to_print, colorbar=True, yaxis=True):
	used_colors = colors#{n: c for n, c in colors.items() if n in to_print}
	best_model = np.array([np.array([
		list(used_colors).index(
			min({ # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
				n: abs(1 - classes[n]().hinv(0.5 if n == "Recursive" else 0, h, m) / sim[str(h)][str(m)] ) for n in to_print
			}.items(), key=operator.itemgetter(1))[0]
		)
	for m in max_hits]) for h in healths])

	cmap = mpl.colors.ListedColormap(list(used_colors.values()))
	boundaries = [-0.5] + [list(used_colors).index(c) + 0.5 for c in used_colors]
	norm = clrs.BoundaryNorm(boundaries, cmap.N, clip=True)
	return ax.imshow(best_model, aspect='auto', origin='lower', cmap=cmap, norm=norm, interpolation='none')

if __name__ == '__main__':
	m_min, m_max = (1, 110)
	h_min, h_max = (1, 255)
	max_hits = np.array(range(m_min, m_max+1))
	healths = np.array(range(h_min, h_max+1))
	Ms, Hs = np.meshgrid(max_hits, healths)

	classes = {name: cl for name, cl in inspect.getmembers(sh, inspect.isclass)}
	sim = load_dataset(N=100_000)

	fig, axes = plt.subplots(nrows=1, ncols=3)
	scale=10
	fig.set_size_inches((1920/1080*scale, scale/2))
	ax1, ax2, ax3 = axes.flat
	ax2.set_yticklabels([])
	ax2.tick_params(axis='y', which='both', left=False, right=False, labelbottom=False)
	ax3.set_yticklabels([])
	ax3.tick_params(axis='y', which='both', left=False, right=False, labelbottom=False)
	ax1.set_ylabel("$h_0$", fontsize=25)
	ax2.set_xlabel("M", fontsize=25)
	ax1.tick_params(axis='y', labelsize=18)
	ax1.tick_params(axis='x', labelsize=18)
	ax2.tick_params(axis='x', labelsize=18)
	ax3.tick_params(axis='x', labelsize=18)

	im = draw(ax3, ["Crude", "Average", "Recursive", "MarkovChainApprox", "MarkovChain"], colorbar=False, yaxis=False)
	draw(ax2, ["Crude", "Average", "Recursive", "MarkovChainApprox"], colorbar=False, yaxis=False)
	draw(ax1, ["Crude", "Average", "Recursive", ], colorbar=False)

	cbar_ax = fig.add_axes([0.12, 0.0, .78, 0.03])
	cb = fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
	cb.set_ticks([list(colors).index(c) for c in colors])
	cb.set_ticklabels([k.replace('MarkovChain', 'MC') for k in colors.keys()])
	cb.ax.tick_params(labelsize=25)
	fig.subplots_adjust(wspace=0.02, bottom=0.2)

	showing = len(sys.argv) >= 2 and sys.argv[1] == 'show'
	if showing:
		plt.show()
	else:
		file_name = "best_model"
		plt.savefig(f"{file_name}.pdf", bbox_inches='tight')
		os.system(f"pdfcrop {file_name}.pdf")
		os.rename(f"{file_name}-crop.pdf", f"{file_name}.pdf")
	plt.close()

