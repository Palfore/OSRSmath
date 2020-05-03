from osrsmath.apps.GUI.optimize.ignore_adjust_skeleton import Ui_IgnoreAdjustPanel
from osrsmath.apps.GUI.shared.widgets import Savable
from PyQt5 import QtCore, QtGui, QtWidgets
import ast
import re

class Data:
	pass

class IgnoreAdjustPanel(QtWidgets.QWidget, Ui_IgnoreAdjustPanel, Savable):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.data = Data()
		self.data.ignore = ''
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
		text = self.entities['ignore_data'].get()
		text = '",\n"'.join([item.strip() for item in text.split('\n')])
		return ast.literal_eval(f'["{text}"]')

	def get_adjust(self):
		text = self.entities['adjust_data'].get()
		first = True

		json_object = {}
		obj = None
		for i, line in enumerate(text.split('\n')):
			assert line.count(':') <= 1, f"Line #{i} shouldn't contain more than 1 ':'"

			# If the ending of a line (ignoring whitespace) is ':{' it signals that the line has an item.
			if re.sub(r"\s+", "", line).endswith(':{'):
				item_name = line.split(':')[0].strip()
				assert item_name not in json_object, f'{item_name} on line #{i} is already specified.'
				obj = {'name': item_name, 'req': {}}
			# If a line has a ':' (without a '{') it contains a requirement
			elif (':' in line) and ('{' not in line):
				left, right = line.split(':', 1)
				assert left.strip() not in obj['req'], f'{left.strip()} on line #{i} (item {obj["name"]}) is already specified.'
				obj['req'].update({left.strip(): int(right.strip(','))})
			# A '}' signals the end of a item creation. It will be added to the collection.
			elif re.sub(r"\s+", "", line).startswith('}'):
				json_object.update({obj['name']: obj['req']})
				obj = None
		return json_object

	def on_toggle_change(self):
		self.set_text(str(self.get_checked('data').get()))

	def update_data_from_text(self, _=None):
		self.get_checked('data').set(self.text.toPlainText())

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
		self.text.setPlainText(text)
		# self.text.setPlainText(json.dumps(text.replace("'", '"'), indent=4).encode('utf-8').decode('unicode_escape').strip('"'))
