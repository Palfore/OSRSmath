import osrsmath.model.damage as damage
from matplotlib import cm
import matplotlib.pyplot as plt
import osrsmath.config as config
import numpy as np
import sys
import os

showing = len(sys.argv) >= 2 and sys.argv[1] == 'show'
fig, ax = config.get_figure(-124, 23, scale=5 if showing else 10)
plt.xlabel("$M$", fontsize=15)
plt.ylabel("$h$", fontsize=15)
ax.set_zlabel("Average Damage", fontsize=15, rotation=90)

h, M = 100, 100
y, x = np.meshgrid(range(h), range(M))
z = np.vectorize(damage.average)(y, x)
surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm)

xs = range(min(h, M))
ax.plot(xs, xs, [damage.average(x, x) for x in xs], linewidth=2, c='black', zorder=3)

if showing:
	plt.show()
else:
	file_name = "average_damage"
	plt.savefig(f"{file_name}.pdf")
	os.system(f"pdfcrop {file_name}.pdf")
	os.rename(f"{file_name}-crop.pdf", f"{file_name}.pdf")