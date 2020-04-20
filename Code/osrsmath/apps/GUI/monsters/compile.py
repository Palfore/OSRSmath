import osrsmath.apps.GUI.config as config
import os

def replace_image_dir(file_path):
	# Replace '../images/' with the code to determine the configured images directory
	injection = "import osrsmath.apps.GUI.config as config"
	with open(f"{file_path}.py", 'w') as f:
		f.write(injection+'\n\n')
		for line in text:
			if ".setPixmap(QtGui.QPixmap(" in line:
				assert '"../images/' in line, f'The default path used in qt-designer could not be found, maybe it changed?'
				line = line.replace('"../images/', f'f"{{config.images_directory}}/')
			f.write(line + '\n')



file_path = 'monsters'
os.system(f"pyuic5 -x {file_path}.ui -o {file_path}.py")
with open(f"{file_path}.py") as f:
	text = f.read().split('\n')


file_path = 'player_stats'
os.system(f"pyuic5 -x {file_path}.ui -o {file_path}.py")