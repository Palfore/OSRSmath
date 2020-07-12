# Useful development commands:
# Install locally pip install -e .
# rm -rf dist/ build/ osrsmath.egg-info/ && python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# pip install --extra-index-url=https://test.pypi.org/simple/ osrsmath==0.1.5
# pip freeze | xargs pip uninstall -y

# On linux sub system (lss) for windows add this to get graphics (matplotlib) support
# sudo apt-get install python3-tk

# On lss, install latex compiler (https://miktex.org/howto/install-miktex-unx)
# sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889
# echo "deb http://miktex.org/download/ubuntu bionic universe" | sudo tee /etc/apt/sources.list.d/miktex.list
# sudo apt-get update
# sudo apt-get install miktex
# miktexsetup
# miktexsetup finish
# initexmf --set-config-value [MPM]AutoInstall=1

# The command line utility `convert` is used.
# sudo apt install imagemagick

# INSTEAD of this, just use lualatex. The below procedure worked on windows, but not lss
# To increase memory capacity of latex to compile large tree diagrams
# without a default editor (?) its in home/.miktex/texmfs/config/miktex/config/pdflatex.ini
# Find the locations of your vim or nano editor using "whereis vim" or "whereis nano"
# initexmf --edit-config-file=pdflatex
# main_memory=10000000  # Add this line!
# initexmf --dump=pdflatex
# pdflatex tree.tex

from setuptools import setup, find_packages

with open('README.md') as f:
	long_description = f.read()

setup(
	name='osrsmath',
	version='0.0.3.3',
	packages=find_packages(),
	description="Mathematical Functions & Optimization Calculations for OSRS",
	long_description_content_type='text/markdown',
	long_description=long_description,
	author="Nawar Ismail",
	author_email="nawar@palfore.com",
	url="https://github.com/Palfore/OSRS-Combat/",
	license='MIT',
	keywords='math optimization old school runescape',
	package_data={
		"osrsmath": [
			"apps/GUI/shared/stylesheets",
			"apps/GUI/shared/stylesheets/*",
			"apps/optimize/data/*",
			"combat/data/*",
		],
	},
	# inlcude_package_data=True,
	classifiers=[
	 	'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Topic :: Scientific/Engineering :: Mathematics',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
	project_urls={
	},
	install_requires=[
		'wheel',
		# 'pathos',  # multiprocess used instead.
		'PySide2',
		'numpy',
		'matplotlib',
		'scipy',
		'Dijkstar',
		'requests',
		'tornado',
		'multiprocess',
                'jsoncomment',
	],  # Developers may need PyInstaller, and Pdoc3
	python_requires='>=3',
)
