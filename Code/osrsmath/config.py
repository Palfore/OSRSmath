import os
import sys
import pathlib
from pathlib import Path

TOP = os.path.dirname(__file__)

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		# Inside this, we store all data in the 'DATA' directory
		base_path = os.path.join(sys._MEIPASS, 'DATA')
	except AttributeError:
		base_path = os.path.abspath(TOP)
		# print('here', TOP, base_path)
	return Path(os.path.join(base_path, relative_path))

import shutil
def user_path(relative_path, default=None):
	# https://stackoverflow.com/questions/1024114/location-of-ini-config-files-in-linux-unix
	try:  # Linux/MacOs
		home = Path(os.environ.get('XDG_DATA_HOME', Path(os.environ['HOME'])/'.local/share'))
	except KeyError:  # Windows
			home = Path(os.environ['APPDATA'])


	home /= 'osrsmath'
	if not home.is_dir():
		home.mkdir()
	user_file = home/relative_path

	if not user_file.is_file() and default:
		# print(f'Attempting to create {relative_path}')
		default = Path(default)
		if not default.is_file():
			raise FileNotFoundError(default)
		# print(default, user_file)
		os.makedirs(user_file.parent, exist_ok=True)
		shutil.copy(default, user_file)
	return user_file

DATA_PATH = os.path.join(TOP, 'model/data')
RESULTS_PATH = os.path.join(TOP, 'results')


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
