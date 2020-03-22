import os
_here = os.path.dirname(__file__)
DATA_PATH = os.path.join(_here, 'Data')
RESULTS_PATH = os.path.join(_here, 'Results')


def get_figure(a=None, e=None, scale=10):
		""" Creates the desired figure setup:
						1) Maximize Figure
						2) Create 3D Plotting Environment
						3) Rotate Z axis label so it is upright
						4) Let labels
						5) Increase label font size
						6) Rotate camera to ideal (predetermined) angle """
		from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
		import matplotlib.pyplot as plt
		import matplotlib as mpl
		mpl.rcParams["savefig.directory"] = "."

		fig = plt.figure()
		fig.set_size_inches(1920/1080*scale, scale)
		ax = fig.add_subplot(111, projection='3d')
		ax.zaxis.set_rotate_label(False)  # disable automatic rotation, otherwise you can't manually override
		ax.xaxis._axinfo['label']['space_factor'] = 6.8
		ax.yaxis._axinfo['label']['space_factor'] = 4.8
		ax.zaxis._axinfo['label']['space_factor'] = 4.8
		ax.view_init(azim=a, elev=e)
		return fig, ax
