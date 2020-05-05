from osrsmath.apps.optimize.gui_single import Ui_MainWindow
from pathlib import Path

from osrsmath.model.player import Player, get_equipment_data
from pprint import pprint as pp
from PyQt5 import QtCore, QtGui, QtWidgets

DATA_PATH = Path().absolute() / 'data'
slots = ['head', 'cape', 'neck', 'ammo', 'weapon', 'body', 'shield', 'legs', 'hands', 'feet', 'ring']

class GUI(Ui_MainWindow):
	HELP_TEXT = """\
		This app allows you to determine the optimal equipment to wear against a set of opponents.

		There are three main sections:
		  1. Player (top left):
		      a) Enter combat levels. Prompts appear if others are needed.
		      b) Ignore equipment you don't want to consider.
		      c) Adjust equipment requirements (if inaccurate or self-imposed)

		  2. Monster (bottom left):
		      a) Lookup by name and (crudely) filter by NMZ bosses.
		      b) If inaccurate or cannot be found, modify values.

		  3. Optimize (right)
		      a) View fighting pool (ie. multiple enemies - useful for NMZ)
		      b) Choose training skill
		      c) Choose potions and how you use them.
		      d) Choose prayers (always on).
		      == Output ==
		      e) Optimal equipment (dropdowns are for possible future use).
		      f) Attack stance, xp/h, and offensive bonuses are also shown.

		Note that there are a lot of exceptions in this game, so the interface is designed to have slack. """

	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)
		self.load_defaults()
		self.monster_panel.add.clicked.connect(self.add_monster)
		self.optimize_panel.evaluate.clicked.connect(self.on_evaluate)
		self.optimize_panel.opponents.itemDoubleClicked.connect(
			lambda item: self.monster_panel.fill_monster(item.text(), self.optimize_panel.data.monsters[item.text()])
		)

		self.optimize_panel.xp_rate.setStyleSheet("color: white;")
		self.optimize_panel.attack_stance.setStyleSheet("color: white;")

		self.on_evaluate()
		import textwrap
		self.menuHelp.triggered.connect(lambda: QtWidgets.QMessageBox(
			QtWidgets.QMessageBox.Information,
			'Help - Overview', textwrap.dedent(self.HELP_TEXT)
		).exec())

		for slot in slots:
			dropdown = getattr(self.optimize_panel, slot)
			dropdown.mouseDoubleClickEvent = lambda _=None, slot=slot: self.ignore_adjust_panel.prepend_text(getattr(self.optimize_panel, slot).currentText())




	def add_monster(self):
		name = self.monster_panel.custom_name.text()
		if name:
			self.optimize_panel.add_monster(name, self.monster_panel.get_monster_as_dict())

	def update_status(self, message):
		self.MainWindow.statusBar().showMessage(message)

	def on_evaluate(self):
		from osrsmath.apps.optimize.logic.optimize import get_sets, get_best_set
		from osrsmath.model.monsters import Monster
		from osrsmath.model.boosts import BoostingSchemes, Prayers, Potions
		import time

		try:
			self.optimize_panel.progressBar.setValue(0)
			equipment_data = get_equipment_data()
			monsters = {name: Monster(**m) for name, m in self.optimize_panel.data.monsters.items()}
			if not monsters:
				QtWidgets.QMessageBox(
					QtWidgets.QMessageBox.Warning, 'Invalid Number of Monsters', "You haven't selected enough monsters."
				).exec()
				return

			# Collect Input
			training_skill = self.optimize_panel.get_training_skill()
			special_sets = self.optimize_panel.get_selected_sets()
			stats = self.player_panel.get_stats()
			stats['current_health'] = int(self.optimize_panel.entities['dharok'].get())

			ignore = self.ignore_adjust_panel.get_ignore()
			adjust = self.ignore_adjust_panel.get_adjust()
			potion = getattr(Potions, self.optimize_panel.potions.currentText())
			potion_attributes = self.optimize_panel.potion_attributes.currentText()
			prayer = getattr(Prayers, self.optimize_panel.prayers.currentText())
			prayer_attributes = self.optimize_panel.prayer_attributes.currentText()
			if self.optimize_panel.boosting_scheme.currentText() == 'Dose After':
				skill = self.optimize_panel.below_skill.currentText()
				redose_level = int(self.optimize_panel.redose_level.text())
				boost = lambda p: BoostingSchemes(p, prayer, prayer_attributes).potion_when_skill_under(
					potion, skill, redose_level, potion_attributes
				)
			else:
				boost = lambda p: BoostingSchemes(p, prayer, prayer_attributes).constant(potion, potion_attributes)

			# Time and Evaluate Solution
			t0 = time.time()
			self.update_status(f'Step (1/2). Generating Sets...')
			sets = get_sets(training_skill, stats, monsters, ignore, adjust, equipment_data, special_sets, progress_callback=lambda i: self.optimize_panel.progressBar.setValue(i))
			t1 = time.time()
			self.update_status(f'Step (2/2). Evaluating {len(sets)} Sets...')
			s, xp, stance = get_best_set(
				stats,
				training_skill,
				boost,
				monsters,
				sets,
				include_shared_xp=False,
				progress_callback=lambda i: self.optimize_panel.progressBar.setValue(i)
			)
			t2 = time.time()
			self.update_status('Finished ...')

			# Display Optimal Equipment
			for slot in slots:
				equipment_list = getattr(self.optimize_panel, slot)
				equipment_list.clear()
				if slot == 'weapon':
					equipment_list.addItem(s.get('weapon') if 'weapon' in s else s.get('2h'))
				else:
					equipment_list.addItem(s.get(slot))

			# Display Offensive Attributes
			tab = self.optimize_panel.best_in_slot_bonuses
			player = Player({})
			for slot, item_name in s.items():
				player.equip_by_name(item_name)
			equipment_stats = player.get_stats()
			for i, stat in enumerate(['attack_stab', 'attack_slash', 'attack_crush', 'attack_ranged', 'attack_magic',
										'melee_strength', 'ranged_strength', 'magic_damage', 'attack_speed']):
				tab.setItem(i, 0, QtWidgets.QTableWidgetItem(str(round(equipment_stats[stat], 2))))
			tab.setItem(9, 0, QtWidgets.QTableWidgetItem(str("")))

			# Additional Messages
			player = Player(stats)
			player.combat_style = stance
			[player.equip_by_name(e) for e in s.values()]
			M = player.get_max_hit(potion, prayer)
			print(M)

			report = f"Solved in {t2-t0:.2f}s ({t1-t0:.2f}s, {t2-t1:.2f}s) using {len(sets)} sets, giving {xp/1000:.2f}k xp/h."
			print(report, stance)
			self.optimize_panel.xp_rate.setText(f"{xp/1000:,.2f}k")
			self.optimize_panel.attack_stance.setText(f"{stance}")
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
			).exec()

	def load_defaults(self):
		self.player_panel.import_defaults(DATA_PATH/'player.json')
		self.ignore_adjust_panel.import_defaults(DATA_PATH/'ignore.json')
		self.optimize_panel.import_defaults(DATA_PATH/'monsters.json')

		self.ignore_adjust_panel.set_text(self.ignore_adjust_panel.get_checked('data').get())

	def save_defaults(self):
		self.player_panel.export_defaults(DATA_PATH/'player.json')
		self.ignore_adjust_panel.export_defaults(DATA_PATH/'ignore.json')
		self.optimize_panel.export_defaults(DATA_PATH/'monsters.json')


if __name__ == '__main__':
	from osrsmath.apps.GUI.shared.application import run
	run(GUI)