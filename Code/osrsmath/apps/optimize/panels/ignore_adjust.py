from osrsmath.apps.GUI.optimize.ignore_adjust_skeleton import Ui_IgnoreAdjustPanel
from osrsmath.apps.GUI.shared.widgets import Savable
from PyQt5 import QtCore, QtGui, QtWidgets
import json

class Data:
	pass

class IgnoreAdjustPanel(QtWidgets.QWidget, Ui_IgnoreAdjustPanel, Savable):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.data = Data()
		self.data.ignore = '[]'
		self.data.adjust = r'{}'
		self.entities = {
			'ignore_data': Savable.Entity(
				None, None,
				lambda o, v: setattr(self.data, 'ignore', v),
				lambda o: self.data.ignore
			),
			'adjust_data': Savable.Entity(
				None, None,
				lambda o, v: setattr(self.data, 'adjust', v),
				lambda o: self.data.adjust
			),
			'ignore_toggle': Savable.Entity(
				self.ignore, True,
				lambda o, v: o.setChecked(v),
				lambda o: o.isChecked()
			),
			'adjust_toggle': Savable.Entity(
				self.adjustments, False,
				lambda o, v: o.setChecked(v),
				lambda o: o.isChecked()
			),
		}

		self.entities['ignore_toggle'].object.toggled.connect(self.on_toggle_change)
		# self.entities['adjust_toggle'].object.toggled.connect(self.on_toggle_change)  # only one required
		self.text.setTabStopDistance(12)
		self.text.focusOutEvent = self.update_data_from_text

	def get_ignore(self):
		return json.loads(self.entities['ignore_data'].get())

	def get_adjust(self):
		return json.loads(self.entities['adjust_data'].get())

	def on_toggle_change(self):
		self.set_text(str(self.get_checked('data').get()))

	def update_data_from_text(self, _=None):
		self.set_text(self.text.toPlainText())
		try:
			data = json.loads(self.text.toPlainText())
			data = json.dumps(data, indent=4)
		except json.decoder.JSONDecodeError as e:
			self.text.setFocus()
			print(e)
			return
		self.get_checked('data').set(data)

	def get_checked(self, kind):
		''' Returns the kind entity whose toggle is checked. '''
		assert kind in ('toggle', 'data')
		if self.entities[f'ignore_toggle'].object.isChecked():
			return self.entities[f'ignore_{kind}']
		elif self.entities[f'adjust_toggle'].object.isChecked():
			return self.entities[f'adjust_{kind}']
		else:
			assert False, 'Neither ignore/adjust checkboxes were selected when updating.'

	def set_text(self, text):
		self.text.setPlainText(json.dumps(text.replace("'", '"'), indent=4).encode('utf-8').decode('unicode_escape').strip('"'))
