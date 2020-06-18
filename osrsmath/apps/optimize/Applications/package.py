from pathlib import Path
import PyInstaller
import os
import json
import osrsmath.config as config

import platform
import shutil
import sys
top = platform.system()

def compile():
	try:
		shutil.rmtree(top)
	except FileNotFoundError:
		pass
	os.makedirs(top)

	try:
		os.chdir(top)
		original_data_path = Path(config.TOP)
		new_data_path = Path('DATA/')
		additional_data = [
			'model/data/',
			'apps/GUI/shared/stylesheets',
			'apps/optimize/data',
		]

		args = [
			'../../main.py',
			'--hiddenimport=pkg_resources.py2_warn',
		#	   '--onefile',
			*[f"--add-data {original_data_path/path}{os.pathsep}{new_data_path/path}" for path in additional_data]
		]
		command = f'''{sys.executable} -m PyInstaller {json.dumps(args).replace('"', '').replace(',', '')[1:-1]}'''
		print(command)
		os.system(command)
	except Exception as e:
		print(e)
	finally:
		os.chdir('../')

def run():
	# print(os.path.abspath('.'))
	os.system(f'./{top}/dist/main/main')

if __name__ == '__main__':
	compile()
	run()