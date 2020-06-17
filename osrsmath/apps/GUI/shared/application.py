from PySide2 import QtCore, QtGui, QtWidgets
from pathlib import Path

import osrsmath.config as config
import sys
import os

def run(main_gui_class):
	# https://leomoon.com/journal/python/high-dpi-scaling-in-pyqt5/
	QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
	QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

	app = QtWidgets.QApplication(sys.argv)

	# START APPLICATION
	MainWindow = QtWidgets.QMainWindow()
	ui = main_gui_class()
	ui.MainWindow = MainWindow  # Allow class to set internals
	ui.setupUi(MainWindow)
	if hasattr(ui, 'save_defaults'):
		MainWindow.closeEvent = lambda self: ui.save_defaults()
	MainWindow.show()

	app.setStyle('Fusion')
	stylesheet_file = config.resource_path("apps/GUI/shared/stylesheets/darkorange.css")
	with open(os.path.abspath(stylesheet_file), "r") as f:
		MainWindow.setStyleSheet(f.read())

	# APPLICATION EXIT
	try:
		ret = app.exec_()
	except:  # This doesn't catch a lot of things, since often abort is called
		if hasattr(ui, 'save_defaults'):
			ui.save_defaults()
		raise
	sys.exit(ret)
