from osrsmath.apps.GUI.optimize.optimize_skeleton import Ui_Form
from osrsmath.apps.GUI.shared.widgets import Savable
from PyQt5 import QtCore, QtGui, QtWidgets

import osrsmath.model.boosts as boosts
import inspect

class Data:
	pass

def disable(obj):
	# obj.setEnabled(False)
	obj.hide()

def enable(obj):
	obj.show()
	# if not obj.isEnabled():
		# obj.setEnabled(True)

class OptimizePanel(QtWidgets.QWidget, Ui_Form, Savable):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.data = Data()
		self.data.monsters = {}

		self.entities = {
			'monsters': Savable.Entity(
				None, None,
				lambda o, v: {self.add_monster(name, monster) for name, monster in v.items()},
				lambda v: self.data.monsters
			),
			'potions': Savable.Entity(
				self.potions, None, lambda o, v: o.setCurrentText(v), lambda o: o.currentText()
			),
			'potion_attributes': Savable.Entity(
				self.potion_attributes, None, lambda o, v: o.setCurrentText(v), lambda o: o.currentText()
			),
			'boosting_scheme': Savable.Entity(
				self.boosting_scheme, None, lambda o, v: o.setCurrentText(v), lambda o: o.currentText()
			),
			'below_skill': Savable.Entity(
				self.below_skill, None, lambda o, v: o.setCurrentText(v), lambda o: o.currentText()
			),
			'redose_level': Savable.Entity(
				self.redose_level, None, lambda o, v: o.setText(v), lambda o: o.text()
			),
			'prayers': Savable.Entity(
				self.prayers, None, lambda o, v: o.setCurrentText(v), lambda o: o.currentText()
			),
			'prayer_attributes': Savable.Entity(
				self.prayer_attributes, None, lambda o, v: o.setCurrentText(v), lambda o: o.currentText()
			),
		}

		for slot in ['head', 'cape', 'neck', 'ammo', 'weapon', 'body', 'legs', 'hands', 'feet', 'ring']:
			equipment_button = getattr(self, f"{slot}_link")
			equipment_button.clicked.connect(
				lambda _, slot=slot: self.open_link(slot)
			)



		potion_names = list(list(zip(*inspect.getmembers(boosts.Potions, predicate=inspect.isfunction)))[0])
		assert 'none' in potion_names
		self.potions.addItem(potion_names.pop(potion_names.index('none')))  # Place 'none' first
		self.potions.addItems(potion_names)

		prayer_names = list(list(zip(*inspect.getmembers(boosts.Prayers, predicate=inspect.isfunction)))[0])
		assert 'none' in prayer_names
		self.prayers.addItem(prayer_names.pop(prayer_names.index('none')))  # Place 'none' first
		self.prayers.addItems(prayer_names)

		self.potions.currentIndexChanged.connect(self.on_potion_select)
		self.boosting_scheme.currentIndexChanged.connect(self.on_boost_scheme_select)
		self.prayers.currentIndexChanged.connect(self.on_prayer_select)
		self.redose_level.setValidator(QtGui.QIntValidator(0, 99))

		self.on_boost_scheme_select()
		self.on_potion_select()
		self.on_prayer_select()

		# Allow the delete key to remove the selected opponent
		shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self.opponents);
		shortcut.activated.connect(self.remove_selected_monster)

	def open_link(self, slot):
		from osrsmath.model.player import get_equipment_by_name
		item = getattr(self, slot).currentText()
		try:
			equipment = get_equipment_by_name(item)
		except ValueError as e:
			print(e)
			return
		from pprint import pprint
		import webbrowser
		pprint(equipment)
		webbrowser.open(get_equipment_by_name(item)['wiki_url'])

	def on_prayer_select(self):
		if self.prayers.currentText() == 'none':
			disable(self.prayer_attributes)
		else:
			enable(self.prayer_attributes)

	def on_potion_select(self):
		if self.potions.currentText() == 'none':
			disable(self.potion_attributes)
			disable(self.boosting_scheme)
		else:
			enable(self.potion_attributes)
			enable(self.boosting_scheme)
		self.on_boost_scheme_select()

	def on_boost_scheme_select(self):
		if self.boosting_scheme.currentText() == 'Constant' or self.potions.currentText() == 'none':
			disable(self.below_skill)
			disable(self.redose_level)
			disable(self.label_5)
		else:
			enable(self.below_skill)
			enable(self.redose_level)
			enable(self.label_5)

	def get_training_skill(self):
		return self.training_skill.currentText().lower()

	def remove_selected_monster(self):
		name = self.opponents.takeItem(self.opponents.currentRow()).text()
		del self.data.monsters[name]

	def add_monster(self, name, monster):
		self.data.monsters[name] = monster
		if name not in (self.opponents.item(i).text() for i in range(self.opponents.count())):
			self.opponents.addItem(name)