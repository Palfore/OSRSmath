""" Contains several useful utility functions for handling the GUI.
	This module can be run to provide some functionality:
		Run: `python util.py make` to compile ALL .ui files into the respective .py files."""
import os
from pathlib import Path

UI_COMPILER = 'pyside2-uic'  # 'pyuic5'
RC_COMPILER = 'pyside2-rcc'  # 'pyrcc5'

def make_ui(file_path):
	os.system(f"{UI_COMPILER} {file_path}.ui -o {file_path}.py")

def make_rc(file_path):
	os.system(f'{RC_COMPILER} {file_path}.qrc -o {file_path}.py')

def make_all(top_level_dir):
	for path in Path(top_level_dir).rglob('*.qrc'):
		print(f"Compiling QRC: {path}")
		extensionless_path = '/'.join(path.parts).rstrip(path.suffix)
		make_rc(extensionless_path)

	for path in Path(top_level_dir).rglob('*.ui'):
		print(f"Compiling UI: {path}")
		extensionless_path = '/'.join(path.parts).rstrip(path.suffix)
		make_ui(extensionless_path)

if __name__ == '__main__':
	import sys
	import osrsmath.config as config
	if len(sys.argv) == 2 and sys.argv[1] == 'make':
		make_all(os.path.join(config.TOP, 'apps'))
