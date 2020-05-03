#  pyuic5 -x gui_skeleton.ui -o gui_skeleton.py && python gui.py

from osrsmath.apps.gui_skeleton import Ui_MainWindow
from osrsmath.apps.optimize.optimize import load, get_sets, get_best_set, load_opponent
from osrsmath.model.experience import combat_level
from PyQt5 import QtCore, QtGui, QtWidgets
from pprint import PrettyPrinter, pprint
import json

class Data:
	def __init__(self):
		self.player_stats, self.opponents, self.ignore, self.adjustments = load(
			R"../results/part_III/optimize/settings.json", process_opponents=False
		)

class GUI(Ui_MainWindow):
	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)
		self.data = Data()

		for i in range(self.best_in_slot.rowCount()):
			self.best_in_slot.verticalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
		for i in range(self.best_in_slot_bonuses.rowCount()):
			self.best_in_slot_bonuses.verticalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
		for i in range(self.best_in_slot_bonuses.rowCount()):
			self.best_in_slot_bonuses.verticalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

		for i in range(self.alternate_gear_bonuses.rowCount()):
			self.alternate_gear_bonuses.verticalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)



		self.player_stats.clicked.connect(lambda enabled: self.changed(enabled, 'player_stats'))
		self.ignore.clicked.connect(lambda enabled: self.changed(enabled, 'ignore'))
		self.adjustments.clicked.connect(lambda enabled: self.changed(enabled, 'adjustments'))
		self.opponents.clicked.connect(lambda enabled: self.changed(enabled, 'opponents'))

		self.input_text_box.focusOutEvent = self.changing_input

		self.evaluate.clicked.connect(self.update)

		self.changed(True, 'player_stats')

	def update(self, enabled):
		opp = {n: load_opponent(s, v) for n, (s, v) in self.data.opponents.items()}
		self.progress_task.setText("Generating Sets (1/2)")
		sets = get_sets(self.data.player_stats, opp, self.data.ignore, self.data.adjustments,
			progress_callback=self.progressBar.setValue)
		self.progress_task.setText("Evaluating Sets (2/2)")
		s, xp, _ = get_best_set(self.data.player_stats, 'attack', lambda p: [(50, 15_000)], opp, sets,
		include_shared_xp=False, progress_callback=self.progressBar.setValue)

		self.progress_task.setText("Waiting to Evaluate...")
		self.progressBar.setValue(0)

		self.best_in_slot.setItem(0, 0, QtWidgets.QTableWidgetItem(s.get('head')))
		self.best_in_slot.setItem(1, 0,QtWidgets.QTableWidgetItem(s.get('cape')))
		self.best_in_slot.setItem(2, 0,QtWidgets.QTableWidgetItem(s.get('neck')))
		self.best_in_slot.setItem(3, 0,QtWidgets.QTableWidgetItem(s.get('ammo')))
		self.best_in_slot.setItem(4, 0,QtWidgets.QTableWidgetItem(s.get('weapon') if 'weapon' in s else s.get('2h')))
		self.best_in_slot.setItem(5, 0,QtWidgets.QTableWidgetItem(s.get('body')))
		self.best_in_slot.setItem(6, 0,QtWidgets.QTableWidgetItem(s.get('legs')))
		self.best_in_slot.setItem(7, 0,QtWidgets.QTableWidgetItem(s.get('hands')))
		self.best_in_slot.setItem(8, 0,QtWidgets.QTableWidgetItem(s.get('feet')))
		self.best_in_slot.setItem(9, 0,QtWidgets.QTableWidgetItem(s.get('ring')))
		self.xp_rate.setText(f"{xp/1000:,.2f}")

	def changed(self, enabled, change):
		if change == 'player_stats':
			self.data.player_stats.update({
				'cmb': combat_level(self.data.player_stats)
			})
			self.input_text_box.setPlainText(json.dumps(self.data.player_stats, indent=0))
		elif change == 'ignore':
			self.input_text_box.setPlainText(json.dumps(self.data.ignore, indent=0))
		elif change == 'adjustments':
			self.input_text_box.setPlainText(json.dumps(self.data.adjustments, indent=0))
		elif change == 'opponents':
			self.input_text_box.setPlainText(json.dumps(self.data.opponents, indent=0))
		else:
			print("Change was unidentified.")

	def changing_input(self, event):
		try:
			if self.player_stats.isChecked():
				self.data.player_stats = json.loads(self.input_text_box.toPlainText())
			elif self.ignore.isChecked():
				self.data.ignore = json.loads(self.input_text_box.toPlainText())
			elif self.adjustments.isChecked():
				self.data.adjustments = json.loads(self.input_text_box.toPlainText())
			elif self.opponents.isChecked():
				self.data.opponents = json.loads(self.input_text_box.toPlainText())
			else:
				print("Change was unidentified.")
		except json.decoder.JSONDecodeError as e:
			QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 'Invalid Json',
                                            f"The json format was incorrect:\n {e}").exec()




if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	# Force the style to be the same on all OSs:
	app.setStyle("Fusion")

	# Now use a palette to switch to dark colors:
	palette = QtGui.QPalette()
	palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
	palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
	palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
	palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
	palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
	palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
	palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
	palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
	palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
	palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
	palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
	palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
	palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
	app.setPalette(palette)


	MainWindow = QtWidgets.QMainWindow()
	ui = GUI()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
