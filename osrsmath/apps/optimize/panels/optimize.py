from osrsmath.apps.GUI.optimize.optimize_skeleton import Ui_Form
from osrsmath.apps.GUI.shared.widgets import Savable
from PySide2 import QtCore, QtGui, QtWidgets

from osrsmath.combat.spells import STANDARD, ANCIENT
from osrsmath.combat.equipment import EquipmentPoolFiltered
import osrsmath.combat.boosts as boosts
import inspect
import webbrowser
import os
from urllib.parse import quote
from pathlib import Path
from pprint import pprint

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
		self.special_sets = [
			'dharok',
			'slayer_helm',
			'obsidian',
			'void_knight',
			'elite_void',
			'berserker_necklace',
			'salve_amulet',
			'thammaron',
			'viggoras',
			'DHL',
			'DHCB',
			'crawsbow',
		]
		self.entities = {
			'monsters': Savable.Entity(
				None, None,
				lambda o, v: {self.add_monster(name, monster) for name, monster in v.items()},
				lambda v: self.data.monsters
			),
			'cpu_cores': Savable.LineEdit(self.cpu_cores, 0),
			'training_skill': Savable.DropDown(self.training_skill, None),
			'potions': Savable.DropDown(self.potions, None),
			'potion_attributes': Savable.DropDown(self.potion_attributes, None),
			'boosting_scheme': Savable.DropDown(self.boosting_scheme, None),
			'below_skill': Savable.DropDown(self.below_skill, None),
			'redose_level': Savable.LineEdit(self.redose_level, None),
			'prayers': Savable.DropDown(self.prayers, None),
			'prayer_attributes': Savable.DropDown(self.prayer_attributes, None),
			'spell': Savable.DropDown(self.spell, None),
			'function': Savable.DropDown(self.function, None),
			'start_end': Savable.LineEdit(self.start_end, 'asd1,1,1-99,99,99'),

			**{s: Savable.CheckBox(getattr(self, s), True) for s in self.special_sets if s != 'dharok'},
			'dharok': Savable.LineEdit(self.dharok, 1),

			'show_histogram': Savable.CheckBox(self.show_histogram, False), 
		}

		for slot in ['head', 'cape', 'neck', 'ammo', 'weapon', 'body', 'legs', 'hands', 'feet', 'ring']:
			getattr(self, f"{slot}_link").setToolTip('Open the wiki page for the equipment in this slot.')
			equipment_button = getattr(self, f"{slot}_link")
			equipment_button.clicked.connect(
				lambda _=None, slot=slot: self.open_link(slot)
			)

		def get_members(cls):
			members = inspect.getmembers(cls, predicate=inspect.isfunction)
			members.sort(key=lambda m: inspect.getsourcelines(m[1])[1])
			names, functions = list(zip(*members))
			return names

		self.potions.addItems(get_members(boosts.Potions))
		self.prayers.addItems(get_members(boosts.Prayers))

		self.function.currentIndexChanged.connect(self.on_function_select)
		self.training_skill.currentIndexChanged.connect(self.on_training_skill_select)
		self.potions.currentIndexChanged.connect(self.on_potion_select)
		self.boosting_scheme.currentIndexChanged.connect(self.on_boost_scheme_select)
		self.prayers.currentIndexChanged.connect(self.on_prayer_select)
		
		self.redose_level.setValidator(QtGui.QIntValidator(0, 99))
		self.cpu_cores.setValidator(QtGui.QIntValidator(0, os.cpu_count()))  # Apparently, it only validate the # of digits
		self.cpu_cores.setToolTip(f'0 will use all cores. You have {os.cpu_count()}.')

		self.on_function_select()
		self.on_training_skill_select()
		self.on_boost_scheme_select()
		self.on_potion_select()
		self.on_prayer_select()

		# Allow the delete key to remove the selected opponent
		shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self.opponents);
		shortcut.activated.connect(self.remove_selected_monster)
		shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Backspace), self.opponents); # For mac
		shortcut.activated.connect(self.remove_selected_monster)

		# Populate spells
		spells = list(STANDARD.keys()) + list(ANCIENT.keys())
		completer = QtWidgets.QCompleter(spells)
		self.spell.clear()
		self.spell.addItems(spells)
		self.spell.setCompleter(completer)
		self.spell.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)


	def get_selected_sets(self):
		return [s for s in self.special_sets if (
			(s == 'dharok' and int(self.entities[s].get())) != 0 or
			(s != 'dharok' and self.entities[s].get())
		)]

	def open_link(self, slot):
		pool = EquipmentPoolFiltered()
		item = getattr(self, slot).currentText()
		try:
			equipment = pool.by_name(item)
		except ValueError as e:
			QtWidgets.QMessageBox(
				QtWidgets.QMessageBox.Warning, 'Wiki Link not Found', str(e)
			).exec_()
			return

		# Encode ending (item name) to "%xx escape" format.
		p = Path(equipment['wiki_url'])
		url = p.parent/quote(p.name)
		webbrowser.open(str(url))

	def on_function_select(self):
		if self.function.currentText() == 'Train':
			self.stackedWidget.setCurrentIndex(0)
		else:
			self.stackedWidget.setCurrentIndex(1)

	def on_training_skill_select(self):
		if self.training_skill.currentText() == 'magic':
			enable(self.spell)
			enable(self.spell_label)
		else:
			disable(self.spell)
			disable(self.spell_label)

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