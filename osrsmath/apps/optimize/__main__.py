import multiprocess
multiprocess.freeze_support()

from osrsmath.apps.optimize.gui_single import Ui_MainWindow
from osrsmath.apps.optimize.logic.optimize import get_sets, get_best_sets
from osrsmath.combat.boosts import BoostingSchemes, Prayers, Potions
from osrsmath.combat.monsters import get_monster_data
from osrsmath.combat.monsters import Monster
from osrsmath.combat.fighter import Fighter
import osrsmath.apps.GUI.resources
import osrsmath.config as config

from PySide2 import QtCore, QtGui, QtWidgets
from pprint import pprint
from pathlib import Path
import textwrap
import time
import glob
import os

slots = ['head', 'cape', 'neck', 'ammo', 'weapon', 'body', 'shield', 'legs', 'hands', 'feet', 'ring']

class GUI(Ui_MainWindow):
	OVERVIEW_TEXT = textwrap.dedent("""\
		This app allows you to determine the optimal equipment to wear against a set of opponents.

		There are three main panels:
		  1. Player (top left):
		      Enter levels, ignore equipment, and adjust requirements.

		  2. Monster (bottom left):
		      Lookup monsters, adjust there stats if desired.
		      Add them to the monster pool.

		  3. Optimize (right)
		      Find optimal equipment to fight the monster pool using your stats.
		      Allows potions, prayers, and equipment sets.
		      Note that the dropdowns are for potential future use.

		You can change the style and zoom in/out using the menubar.
		This helps people with different monitors/preferences.
		""")

	SHORTCUTS_TEXT = textwrap.dedent("""\
		General:
			Ctrl++ Zoom in
			Ctrl+- Zoom out

		Monster Panel:
			DoubleClick Edit Monster (use it in monster panel to customize)
			Delete Delete selected monster from pool

		Optimize Panel:
			Shift+Enter Evaluate current configuration

			You can also add equipment to the ignore/adjust lists by
			clicking on the dropdown item and using one of:
				Shift+Click Add to ignore
				Ctrl+Click Add to adjust

		""").replace('\t', ' '*6)


	PLAYER_TEXT = textwrap.dedent("""\
		1. Enter your combat stats.
		If additional skill levels are needed you will be asked.
		Username lookup to load your stats is not current implemented.

		2. Equipment listed in the Ignore tab won't be considered.
		Try running the evaluation first, then adding things you want to ignore.
		Lines starting with # are ignored (so you can use them as comments).
		You can use '*' as a wildcard. So "*sword" will ignore anything ending with sword.

		3. Equipment in the Adjust tab will use the given requirements.
		This overrides the database which may have errors, or you may want to impose your own restrictions (e.g. fire cape has no explicit requirements, so you may want to adjust that).
		However, you might find ignore to be much easier to use.
		""").replace('\t', ' '*6)

	MONSTER_TEXT = textwrap.dedent("""\
		Search for monsters.
		The number corresponds to their id.
		The database isn't perfect, so you can look up monsters on the wiki.
		If anything is off, adjust the stats.
		Give an optional name, and add it to the pool.

		You can filter to only show NMZ bosses.
		Due to database restrictions this is only crude.

		Adding a monster to the pool with the same name will override.
		Double clicking a monster in the pool will load it back into this panel.
		This allows you to adjust or view their stats.
		""").replace('\t', ' '*6)

	OPTIMIZE_TEXT = textwrap.dedent("""\
		1. Choose a skill to train (range & mage unsupported now)

		2. Choose a potion, and what it boosts, and how you use it.
		Dose after means:
			"Take a dose after the [skill] *boost* drops below [a threshold]".
			Useful for normal potion usage. Constant is better for overloads.
			If the skill isn't actually boosted, it will just use the boost countdown
			for that skill using the selected potion.

		3. Choose a prayer, and what it boosts.
			level1,2,3 are the successive prayers.

		4. Choose what special sets to consider.
			<Dharok HP> should be the average hp while dh'ing.
			Zero means don't consider dh.

		5. Evaluate. Optionally a histogram can be displayed showing the xp/h distribution.
		===========================

		Each slot label will lookup the corresponding equipment on the wiki.
		Dropdowns are for future consideration.
		Kill information assumes 4xp/hit for all monsters (temporary).
		Kill information counts one kill as the entire pool.
		Offensive bonuses are shown, cost doesn't work.
		""").replace('\t', ' '*6)

	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)

		icon = QtGui.QIcon()
		icon.addFile(str(config.resource_path("apps/GUI/images/logo.png")), QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)

		self.load_defaults()
		self.loadouts = []
		self.monster_panel.add.clicked.connect(self.add_monster)
		self.optimize_panel.evaluate.clicked.connect(self.on_evaluate)
		self.optimize_panel.dec_selected_set.clicked.connect(lambda: self.change_selected_set(change=-1))
		self.optimize_panel.inc_selected_set.clicked.connect(lambda: self.change_selected_set(change=+1))
		self.optimize_panel.selected_set_index.returnPressed.connect(
			lambda: self.change_selected_set(index=int(self.optimize_panel.selected_set_index.text()))
		)
		self.optimize_panel.opponents.itemDoubleClicked.connect(
			lambda item: self.monster_panel.fill_monster(item.text(), self.optimize_panel.data.monsters[item.text()])
		)
		self.optimize_panel.selected_set_index.setValidator(QtGui.QIntValidator())

		self.actionOverview.triggered.connect(lambda: QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
			'Help - Overview', self.OVERVIEW_TEXT
		).exec_())
		self.actionPlayer_Panel.triggered.connect(lambda: QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
			'Help - Player Panel', self.PLAYER_TEXT
		).exec_())
		self.actionMonster_Panel.triggered.connect(lambda: QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
			'Help - Monster Panel', self.MONSTER_TEXT
		).exec_())
		self.actionOptimize_Panel.triggered.connect(lambda: QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
			'Help - Optimize Panel', self.OPTIMIZE_TEXT
		).exec_())
		self.actionShortcuts.triggered.connect(lambda: QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
			'Help - Shortcuts', self.SHORTCUTS_TEXT
		).exec_())

		def update(do):
			if do:
				self.update_status('Updating Equipment...')  # These don't seem to work
				get_equipment_data(force_update=True)
				self.update_status('Updating Monsters...')
				get_monster_data(force_update=True)
				self.update_status('Finished Updating Database!')  # but this does.

		self.actionUpdate_Now.triggered.connect(lambda: update(QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question,
			'Update Now', "Would you like to download the latest equipment and monsters? You only need to do this "
			"if you want to use those new entities. "
			"If something is missing after updating, it is also possible that the osrsbox database has not yet been updated. "
			"Try again on another day.",
			QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
		).exec_() == QtWidgets.QMessageBox.Yes))

		self.optimize_panel.evaluate.setToolTip("Determine the optimal gear for your configuration.")
		self.optimize_panel.dharok.setToolTip("What's your average hp? 0 means don't consider dharok.")
		self.optimize_panel.obsidian.setToolTip("The obsidian armour set, along with the necklace.")

		shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Shift+Return"), self.optimize_panel);
		shortcut.activated.connect(self.on_evaluate)

		def update_style(style_sheet_text=None):
			if style_sheet_text is None:
				style_sheet_text = self.MainWindow.styleSheet()
			self.MainWindow.setStyleSheet(style_sheet_text + '\n' + f'QWidget{{font-size: {self.fontsize}px;}}')

		def increase():
			self.fontsize += 1
			update_style()

		def decrease():
			if self.fontsize > 2:
				self.fontsize -= 1
			update_style()

		# Allow font size changes in menu
		self.fontsize = self.MainWindow.font().pointSize()
		self.actionIncrease_Size.setShortcut("Ctrl++")
		self.actionDecrease_Size.setShortcut("Ctrl+-")
		self.actionIncrease_Size.triggered.connect(increase)
		self.actionDecrease_Size.triggered.connect(decrease)

		# Load stylesheet options into menu
		for style_sheet in glob.glob(str(config.resource_path("apps/GUI/shared/stylesheets/*.?ss"))):
			option = os.path.basename(style_sheet).split('.')[0]  # Raw file name, no extension
			name = f'style_{option}'
			setattr(self, name, QtWidgets.QAction(self.MainWindow))
			item = getattr(self, name)
			item.setObjectName(name)
			item.setText(option)
			self.menuView.addAction(item)
			item.triggered.connect(lambda _=None, style_sheet=style_sheet: update_style(open(style_sheet).read()))


		# Ctrl+click and shift+click equipment adds it to ignore/adjust panel respectively
		def modifier(slot):
			mods = QtWidgets.QApplication.keyboardModifiers()
			if mods == QtCore.Qt.ShiftModifier:
				modify_text = self.ignore_adjust_panel.prepend_ignore
			elif mods == QtCore.Qt.ControlModifier:
				modify_text = self.ignore_adjust_panel.prepend_adjust
			else:
				return
			modify_text(getattr(self.optimize_panel, slot).currentText())

		for slot in slots:
			dropdown = getattr(self.optimize_panel, slot)
			dropdown.activated.connect(lambda _=None, slot=slot: modifier(slot))

	def add_monster(self):
		name = self.monster_panel.custom_name.text()
		if name:
			self.optimize_panel.add_monster(name, self.monster_panel.get_monster_as_dict())

	def update_status(self, message):
		self.MainWindow.statusBar().showMessage(message)

	def on_evaluate(self):
		try:
			self.optimize_panel.progressBar.setValue(0)
			self.monsters = {name: Monster(**m) for name, m in self.optimize_panel.data.monsters.items()}
			if not self.monsters:
				QtWidgets.QMessageBox(
					QtWidgets.QMessageBox.Warning, 'Invalid Number of Monsters', "You haven't selected enough monsters."
				).exec_()
				return

			# Collect Input
			training_skill = self.optimize_panel.get_training_skill()
			special_sets = self.optimize_panel.get_selected_sets()
			stats = self.player_panel.get_stats()
			stats['current_health'] = int(self.optimize_panel.entities['dharok'].get())

			ignore = self.ignore_adjust_panel.get_ignore()
			adjust = self.ignore_adjust_panel.get_adjust()
			
			potion_name = self.optimize_panel.potions.currentText()
			if (potion_name == 'magic' and training_skill != 'magic') or (potion_name == 'ranging' and training_skill != 'ranged'):
				QtWidgets.QMessageBox(
					QtWidgets.QMessageBox.Warning, 'Invalid Potion Input', "The potion you are using doesn't match the training skill."
				).exec_()
				return
			potion = getattr(Potions, potion_name)
			potion_attributes = self.optimize_panel.potion_attributes.currentText()
		
			prayer_name = self.optimize_panel.prayers.currentText()
			if (prayer_name == 'augury' and training_skill not in ['magic', 'magic and defence']) or\
				 (prayer_name == 'rigour' and training_skill not in ['ranged', 'ranged and defence']) or\
				 	((prayer_name == 'chivalry' or prayer_name == 'piety') and training_skill not in ['attack', 'strength', 'defence', 'controlled']):
				QtWidgets.QMessageBox(
					QtWidgets.QMessageBox.Warning, 'Invalid Potion Input', "The prayer you are using doesn't match the training skill."
				).exec_()
				return
			prayer = getattr(Prayers, prayer_name)
			prayer_attributes = self.optimize_panel.prayer_attributes.currentText()
			
			if potion != Potions.none and self.optimize_panel.boosting_scheme.currentText() == 'Dose After':
				below_skill = self.optimize_panel.below_skill.currentText()
				try:
					redose_level = int(self.optimize_panel.redose_level.text())
				except ValueError:
					QtWidgets.QMessageBox(
						QtWidgets.QMessageBox.Warning, 'Invalid Boosting Input', "You haven't provided a valid 'dose after' level."
					).exec_()
					return
				boost = lambda p: BoostingSchemes(p, prayer, prayer_attributes).potion_when_skill_under(
					potion, below_skill, redose_level, potion_attributes
				)
			else:
				boost = lambda p: BoostingSchemes(p, prayer, prayer_attributes).constant(potion, potion_attributes)

			self.fighter = Fighter(stats)
			self.fighter.set_spell(self.optimize_panel.entities['spell'].get() if 'magic' in training_skill else None)
			
			# Time and Evaluate Solution
			t0 = time.time()
			self.update_status(f'Step (1/2). Generating Sets...')
			sets = get_sets(training_skill, stats, self.monsters, ignore, adjust,
				special_sets, progress_callback=lambda i: self.optimize_panel.progressBar.setValue(int(i))
			)
			t1 = time.time()
			self.update_status(f'Step (2/2). Evaluating {len(sets)} Sets...')
			self.loadouts = get_best_sets(  # [(s, xp, stance), ...]
				self.fighter,
				training_skill,
				boost,
				self.monsters,
				sets,
				include_shared_xp=False,
				progress_callback=lambda i: self.optimize_panel.progressBar.setValue(int(i)),
				num_cores=int(self.optimize_panel.cpu_cores.text())
			)
			t2 = time.time()
			self.update_status('Finished ...')
			
			if not self.loadouts:
				self.update_status('No results found.')
				return

			if self.optimize_panel.show_histogram.isChecked():
				import matplotlib.pyplot as plt
				plt.title('Xp/h Histogram')
				plt.ylabel('Frequency')
				plt.xlabel('Xp/h')
				plt.hist([xp for x, xp, stance in self.loadouts])
				plt.show()

			self.optimize_panel.num_sets.setText(f"{len(self.loadouts)} Sets")
			self.display_equipment(0)
			report = f"Solved in {t2-t0:.2f}s ({t1-t0:.2f}s, {t2-t1:.2f}s) using {len(self.loadouts)} sets"
			print(report)
			self.update_status(report)
		except Exception as e:
			import traceback
			tb = traceback.format_exc()
			print(e)
			print(tb)
			self.update_status('Error Encountered')
			QtWidgets.QMessageBox(
				QtWidgets.QMessageBox.Critical,
				'Error Encountered',
				f"{e}\n{tb}"
			).exec_()

	def change_selected_set(self, change=None, index=None):
		if change is None and index is None:
			raise ValueError("Only one of change or index can be specified.")

		if change is not None:
			if not self.loadouts:
				return
			if len(self.loadouts) == 0:
				return
			elif len(self.loadouts) == 1:
				i = 0
			else:
				i = int(self.optimize_panel.selected_set_index.text())
				i = (i + change) % len(self.loadouts)
		elif index is not None:
			i = max(0, min(index, len(self.loadouts)-1))
		else:
			assert False, "Logic Error!"
		self.optimize_panel.selected_set_index.setText(str(i))
		self.display_equipment(i)

	def display_equipment(self, i):
		if not self.loadouts:
			return
		self.optimize_panel.selected_set_index.setText(str(i))
		loadout, xp, stance = self.loadouts[i]
		for slot in slots:
			equipment_list = getattr(self.optimize_panel, slot)
			equipment_list.clear()
			if slot == 'weapon':
				equipment_list.addItem(loadout.get('weapon') if 'weapon' in loadout else loadout.get('2h'))
			else:
				equipment_list.addItem(loadout.get(slot))

		# Display Offensive Attributes
		tab = self.optimize_panel.best_in_slot_bonuses
		self.fighter.equipment.undress()
		self.fighter.equipment.wear(*list(loadout.values()))
		self.fighter.set_stance(stance)
		equipment_stats = self.fighter.equipment.get_stats()
		for i, stat in enumerate(['attack_stab', 'attack_slash', 'attack_crush', 'attack_ranged', 'attack_magic',
									'melee_strength', 'ranged_strength', 'magic_damage', 'attack_speed']):
			tab.setItem(i, 0, QtWidgets.QTableWidgetItem(str(round(equipment_stats[stat], 2))))
		tab.setItem(9, 0, QtWidgets.QTableWidgetItem(str("")))

		hit_rate = xp/4  # Assume 4xp per hit
		total_hitpoints = sum(monster.levels['hitpoints'] for name, monster in self.monsters.items())
		kill_time = total_hitpoints / hit_rate
		self.optimize_panel.xp_rate.setText(f"{xp/1000:,.2f}k")
		self.optimize_panel.attack_stance.setText(f"{stance}")
		self.optimize_panel.kill_time.setText(f"{3600*kill_time:,.2f}s")
		self.optimize_panel.kills_per_hour.setText(f"{1/kill_time:,.2f}")


	def get_data_path(self, file):
		return config.resource_path(f"apps/optimize/data/{file}")

	def load_defaults(self):
		self.player_panel.import_defaults(self.get_data_path('player.json'))
		self.ignore_adjust_panel.import_defaults(self.get_data_path('ignore.json'))
		self.optimize_panel.import_defaults(self.get_data_path('monsters.json'))

		self.ignore_adjust_panel.set_text(self.ignore_adjust_panel.get_checked('data').get())

	def save_defaults(self):
		self.player_panel.export_defaults(self.get_data_path('player.json'))
		self.ignore_adjust_panel.export_defaults(self.get_data_path('ignore.json'))
		self.optimize_panel.export_defaults(self.get_data_path('monsters.json'))



if __name__ == '__main__':
	import multiprocess
	multiprocess.freeze_support()
	from osrsmath.apps.GUI.shared.application import run
	run(GUI)