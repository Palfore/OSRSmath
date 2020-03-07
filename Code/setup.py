# Useful development commands:
# rm -rf dist/ build/ osrsmath.egg-info/ && python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# pip install --extra-index-url=https://test.pypi.org/simple/ osrsmath==0.1.5
# pip freeze | xargs pip uninstall -y
from setuptools import setup, find_packages

with open('README.md') as f:
	long_description = f.read()

setup(
	name='osrsmath',
	version='0.1.6',
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
		"": ["Data/*.json", "Data/*.dat"],
	},
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
	install_requires=['numpy', 'matplotlib', 'scipy', 'Dijkstar', 'requests'],
	python_requires='>=3',
)