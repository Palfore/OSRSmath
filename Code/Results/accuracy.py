from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')
import numpy as np

def Acc(a, d):
    A_greater = 1 - 0.5 * (d + 2) / (a + 1)
    A_lesser = a / (2 * d + 2)
    return A_greater if a >= d else A_lesser

a = range(1000)
d = range(1000)
a, d = np.meshgrid(a, d)
A = np.vectorize(Acc)(a, d)


plt.xlabel("$A_{max}$")
plt.ylabel("$D_{max}$")
ax.set_zlabel("Accuracy", rotation=90)
# plt.zticks(rotation=90)
surf = ax.plot_surface(a, d, A, cmap=cm.coolwarm)

ax.plot([1000], [1000], [1.01])
ax.plot(range(1000), range(1000), [Acc(x, x) for x in range(1000)], linewidth=2, c='black', zorder=3)
plt.show()
plt.savefig("Accuracy.svg")
plt.savefig("Accuracy.ps")
plt.savefig("Accuracy.png")
plt.savefig("Accuracy.eps")
plt.savefig("Accuracy.pdf")