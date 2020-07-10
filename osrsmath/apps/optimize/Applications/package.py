from pathlib import Path
import PyInstaller
import os
import json
import osrsmath.config as config

import platform
import shutil
import sys
top = system = platform.system()

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
			'combat/data/',
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

		if system in ['Linux', 'Darwin']:
			# Create shortcut, I could not get symlinks to work.
			# This wont work if they don't execute from the top directory.
			with open('osrsmath-optimize', 'w') as f:
				f.write('#!/bin/sh\n')
				f.write('cd "$(dirname $0)/dist/main && ./main')
			os.system('chmod +x osrsmath-optimize')
		elif system == 'Windows':
			os.system(R'mklink "osrsmath-optimize" "dist\main\main.exe"')



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