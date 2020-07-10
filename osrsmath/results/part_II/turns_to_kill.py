from osrsmath.combat.successful_hits import *
from matplotlib import cm
import matplotlib.pyplot as plt
import osrsmath.config as config
import numpy as np
import sys
import os

def plot(m_bounds, h_bounds):
	m_min, m_max = m_bounds
	h_min, h_max = h_bounds
	max_hits = np.array(range(m_min, m_max+1))
	healths = np.array(range(h_min, h_max+1))
	Ms, Hs = np.meshgrid(max_hits, healths)
	fig, ax = config.get_figure(50, 18, scale=5 if showing else 10)
	plt.xlabel("$h_0$", fontsize=25, labelpad=20)
	plt.ylabel("$M$", fontsize=25, labelpad=20)
	ax.set_zlabel("Turns to kill", fontsize=25, rotation=90, labelpad=20)
	ax.tick_params(axis='z', labelsize=18)
	ax.tick_params(axis='y', labelsize=18)
	ax.tick_params(axis='x', labelsize=18)

	A = np.vectorize(lambda m, h: MarkovChain().turns_to_kill(m, h))(Hs, Ms)
	surf = ax.plot_surface(Hs, Ms, A, cmap=cm.hot)

	A = np.vectorize(lambda m, h: Crude().turns_to_kill(m, h))(Hs, Ms)
	surf = ax.plot_surface(Hs, Ms, A, cmap=cm.cool)
	return plt

if __name__ == '__main__':
	showing = len(sys.argv) >= 2 and sys.argv[1] == 'show'
	if showing:
		plot(m_bounds=(1, 110), h_bounds=(1, 250)).show()
		plot(m_bounds=(20, 110), h_bounds=(1, 110)).show()
	else:
		plot(m_bounds=(1, 110), h_bounds=(1, 250))
		file_name = "turns_to_kill"
		plt.savefig(f"{file_name}.pdf")
		os.system(f"pdfcrop {file_name}.pdf")
		os.rename(f"{file_name}-crop.pdf", f"{file_name}.pdf")

		plot(m_bounds=(20, 110), h_bounds=(1, 110))
		file_name = "turns_to_kill_zoom"
		plt.savefig(f"{file_name}.pdf")
		os.system(f"pdfcrop {file_name}.pdf")
		os.rename(f"{file_name}-crop.pdf", f"{file_name}.pdf")
