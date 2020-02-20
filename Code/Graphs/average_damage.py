from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')
import numpy as np

def Acc(M, h):
    upper_D = 0.5*M
    lower_D = 0.5*h*(2 - (h+1)/(M+1))
    return upper_D / M if h >= M else lower_D / M

a = range(100)
d = range(100)
a, d = np.meshgrid(a, d)
A = np.vectorize(Acc)(a, d)


plt.xlabel("$M$")
plt.ylabel("$h$")
ax.set_zlabel("$\left \langle D \\right \\rangle$", rotation=90)
# plt.zticks(rotation=90)
surf = ax.plot_surface(a, d, A, cmap=cm.coolwarm)

ax.plot([100], [100], [1.01])
ax.plot(range(100), range(100), [Acc(x, x) for x in range(100)], linewidth=2, c='black', zorder=3)
plt.show()
plt.savefig("Accuracy.svg")
plt.savefig("Accuracy.ps")
plt.savefig("Accuracy.png")
plt.savefig("Accuracy.eps")
plt.savefig("Accuracy.pdf")