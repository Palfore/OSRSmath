from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import sys

def run(main_gui_class):
	# Style from https://github.com/Lumyo/darkorange-pyside-stylesheet/tree/master/darkorange
	app = QtWidgets.QApplication(sys.argv)
	stylesheet_file = Path(__file__).parent/"stylesheets"/"darkorange"/"darkorange.css"
	with open(stylesheet_file, "r") as f:
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
