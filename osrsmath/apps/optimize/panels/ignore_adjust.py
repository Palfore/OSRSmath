from osrsmath.apps.GUI.optimize.ignore_adjust_skeleton import Ui_IgnoreAdjustPanel
from osrsmath.apps.GUI.shared.widgets import Savable
from PySide2 import QtCore, QtGui, QtWidgets
import ast
import re

class Data:
	pass

class IgnoreAdjustPanel(QtWidgets.QWidget, Ui_IgnoreAdjustPanel, Savable):
	IGNORE_USER_SIGNAL_TEXT = 'USER IGNORES'
	IGNORE_DEFAULT_SIGNAL_TEXT = 'DEFAULT IGNORES'
	ADJUST_USER_SIGNAL_TEXT = 'USER OVERRIDES'
	ADJUST_DEFAULT_SIGNAL_TEXT = 'DEFAULT OVERRIDES'

	IGNORE_TOOLTIP = "Equipment listed here won't be considered."
	ADJUST_TOOLTIP = "Equipment requirements here will override the database."

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
		self.text.textChanged.connect(self.update_data_from_text)

		self.entities['ignore_toggle'].object.setToolTip(self.IGNORE_TOOLTIP)
		self.entities['adjust_toggle'].object.setToolTip(self.ADJUST_TOOLTIP)


	def get_ignore(self):
		text = self.entities['ignore_data'].get()
		text = '",\n"'.join([line.strip() for line in text.split('\n') if not any([
			line.startswith('#'),
			self.IGNORE_USER_SIGNAL_TEXT in line,
			self.IGNORE_DEFAULT_SIGNAL_TEXT in line
		])])
		return ast.literal_eval(f'["{text}"]')

	def get_adjust(self):
		text = self.entities['adjust_data'].get()
		first = True

		json_object = {}
		obj = None
		for i, line in enumerate(text.split('\n')):
			if self.ADJUST_USER_SIGNAL_TEXT in line:
				continue
			if self.ADJUST_DEFAULT_SIGNAL_TEXT in line:
				continue
			if line.startswith('#'):
				continue
			assert line.count(':') <= 1, f"Line #{i} shouldn't contain more than 1 ':'"

			# If the ending of a line (ignoring whitespace) is ':{' it signals that the line has an item.
			if re.sub(r"\s+", "", line).endswith(':{'):
				item_name = line.split(':')[0].strip()
				assert item_name not in json_object, f'{item_name} on line #{i} is already specified.'
				obj = {'name': item_name, 'req': {}}
			# If a line has a ':' (without a '{') it contains a requirement
			elif (':' in line) and ('{' not in line):
				if 'req' not in obj:
					raise ValueError(f"The ':' character shouldn't appear in line {i}: {line.strip()}")
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

	def prepend_ignore(self, item):
		self.entities['ignore_toggle'].object.setChecked(True)
		self._prepend(item, self.IGNORE_USER_SIGNAL_TEXT)

	def prepend_adjust(self, item):
		self.entities['adjust_toggle'].object.setChecked(True)
		self._prepend(f"{item}: {{\n\t\n}}", self.ADJUST_USER_SIGNAL_TEXT)

	def _prepend(self, insertion, insert_signal_text):
		original = self.get_checked('data').get().split('\n')
		for i, line in enumerate(original):
			if line.startswith(insert_signal_text):
				self.set_text('\n'.join(original[:i+1] + [insertion] + original[i+1:]))
				break
		else:  # If you didn't find that flag, just prepend it
			self.set_text(insertion+'\n'+'\n'.join(original))
		self.update_data_from_text()