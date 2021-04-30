from osrsmath.skills.combat.accuracy import accuracy
from matplotlib import cm
import matplotlib.pyplot as plt
import osrsmath.config as config
import numpy as np
import sys
import os

if __name__ == '__main__':
	showing = len(sys.argv) >= 2 and sys.argv[1] == 'show'

	a = range(1000)
	d = range(1000)
	a, d = np.meshgrid(a, d)
	A = np.vectorize(accuracy)(a, d)

	fig, ax = config.get_figure(-168, 25, scale=5 if showing else 10)
	plt.xlabel("$A_{max}$", fontsize=15)
	plt.ylabel("$D_{max}$", fontsize=15)
	ax.set_zlabel("Accuracy", fontsize=15, rotation=90)
	surf = ax.plot_surface(a, d, A, cmap=cm.coolwarm)


	ax.plot([1000], [1000], [1.01])
	ax.plot(range(1000), range(1000), [accuracy(x, x) for x in range(1000)], linewidth=2, c='black', zorder=3)

	if showing:
		plt.show()
	else:
		file_name = "Accuracy"
		plt.savefig(f"{file_name}.pdf")
		os.system(f"pdfcrop {file_name}.pdf")
		os.rename(f"{file_name}-crop.pdf", f"{file_name}.pdf")