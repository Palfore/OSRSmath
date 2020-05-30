from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import sys
import osrsmath.config as config

def run(main_gui_class):
	# Style from https://github.com/Lumyo/darkorange-pyside-stylesheet/tree/master/darkorange
	import os
	# print(os.getcwd(), Path(__file__).parent)
	# print(Path(sys.argv[0]).parent /"stylesheets"/"darkorange"/"darkorange.css")
	# print()
	app = QtWidgets.QApplication(sys.argv)
	# stylesheet_file = Path(__file__).parent/"stylesheets"/"darkorange"/"darkorange.css"
	# stylesheet_file = Path(sys.argv[0]).parent / Path("DATA/apps/GUI/shared/stylesheets/darkorange/darkorange.css")
	print(getattr(sys, '_MEIPASS', None))
	print(Path(sys.argv[0]))
	print(Path(__file__))
	print(__file__)
	print(sys.executable)



	stylesheet_file = config.resource_path("apps/GUI/shared/stylesheets/darkorange/darkorange.css")
	print('stylesheet', stylesheet_file)
	print('>>>', os.path.abspath(stylesheet_file))
	with open(os.path.abspath(stylesheet_file), "r") as f:
		app.setStyleSheet(f.read())

	# START APPLICATION
	MainWindow = QtWidgets.QMainWindow()
	ui = main_gui_class()
	ui.MainWindow = MainWindow
	ui.setupUi(MainWindow)
	if hasattr(ui, 'save_defaults'):
		MainWindow.closeEvent = lambda self: ui.save_defaults()
	MainWindow.show()

	# APPLICATION EXIT
	try:
		ret = app.exec_()
	except:  # This doesn't catch a lot of things, since often abort is called
		if hasattr(ui, 'save_defaults'):
			ui.save_defaults()
		raise
	sys.exit(ret)
