""" Contains several useful utility functions for handling the GUI.
	This module can be run to provide some functionality:
		Run: `python util.py make` to compile ALL .ui files into the respective .py files."""
import os
from pathlib import Path

COMPILER = 'pyuic5'

def make(file_path):
	_make(file_path)
	replace_image_dir(file_path)

def _make(file_path):
	os.system(f"{COMPILER} -x {file_path}.ui -o {file_path}.py")

def make_all(top_level_dir):
	for path in Path(top_level_dir).rglob('*.ui'):
		extensionless_path = '/'.join(path.parts).rstrip(path.suffix)
		make(extensionless_path)

def replace_image_dir(file_path):
	""" When the .ui generates a .py file, the image paths are specific to where they were loaded in
		the Designer app. This is a problem because the file may be loaded from different directories.
		This function will replace the 'hardcoded' path with a function call to the configured
		image directory from config.py. """
	imports = "import osrsmath.apps.GUI.config as config"
	function_call = ".setPixmap(QtGui.QPixmap("
	ending = '))\n'
	with open(f"{file_path}.py", 'r') as f:
		text = f.readlines()

	with open(f"{file_path}.py", 'w') as f:
		f.write(imports+'\n\n')
		for line in text:
			if function_call in line:
				# Since all images must be stored in the images directory, 'images' will always
				# be part of the path, so we can replace the relative parents with the config value.
				widget, image_path = line.split(function_call)
				image_path = Path(image_path.strip(ending)).parts
				assert 'images' in image_path, f'In {file_path}.py, the default path used in qt-designer could not be found, maybe it changed?'
				index = image_path.index('images')

				image_path = '/'.join([f'f"{{config.images_directory}}', *image_path[index+1:]])
				line = widget + function_call + image_path + ending
			f.write(line)

if __name__ == '__main__':
	import sys
	import osrsmath.config as config
	if len(sys.argv) == 2 and sys.argv[1] == 'make':
		make_all(os.path.join(config.TOP, 'apps'))