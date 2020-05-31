""" Using relative links for images is difficult since there is no universal anchor/root.
	This will replace the text 'HEAD' in a image reference so that it begins at osrsmath/.

	eg: In a docstring, the following text:
		.. figure:: HEAD/apps/GUI/images/skill_icons/Farming.png
	will reference the correct image location.
"""

from glob import glob
import osrsmath.config as config
import os

if __name__ == '__main__':
	for path in glob(f'{config.TOP}/docs/**/*.html', recursive=True):
		modified = False
		text = []
		for line in open(path):
			if 'src="HEAD' in line:
				rel = os.path.relpath(config.TOP+'/docs/', path)
				line = line.replace('src="HEAD', f'src="{rel}')
				modified = True
			text.append(line)

		if modified:
			with open(path, 'w') as f:
				f.writelines(text)
