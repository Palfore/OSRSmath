from osrsmath.apps.optimize.gui_single import Ui_MainWindow
from pathlib import Path

from osrsmath.model.player import Player, get_equipment_data
from pprint import pprint as pp
from PyQt5 import QtCore, QtGui, QtWidgets

DATA_PATH = Path().absolute() / 'data'

class GUI(Ui_MainWindow):
	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)
		self.load_defaults()
		self.monster_panel.add.clicked.connect(self.add_monster)
		self.optimize_panel.evaluate.clicked.connect(self.on_evaluate)

		self.optimize_panel.xp_rate.setStyleSheet("color: white;")
		self.optimize_panel.attack_stance.setStyleSheet("color: white;")

		self.on_evaluate()

	def add_monster(self):
		name = self.monster_panel.custom_name.text()
		if name:
			self.optimize_panel.add_monster(name, self.monster_panel.get_monster_as_dict())

	def on_evaluate(self):
		from osrsmath.apps.optimize.logic.optimize import get_sets, get_best_set, load_opponent
		from osrsmath.model.monsters import Monster
		from osrsmath.model.boosts import BoostingSchemes, Prayers, Potions
		import time

		equipment_data = get_equipment_data()
		monsters = {name: Monster(**m) for name, m in self.optimize_panel.data.monsters.items()}
		training_skill = self.optimize_panel.get_training_skill()
		stats = self.player_panel.get_stats()
		ignore = self.ignore_adjust_panel.get_ignore()
		adjust = self.ignore_adjust_panel.get_adjust()

		t0 = time.time()
		sets = get_sets(stats, monsters, ignore, adjust, equipment_data)#progress_callback=lambda i: self.optimize_panel.progressBar.setValue(i))
		s, xp, stance = get_best_set(
			stats,
			training_skill,
			lambda p: BoostingSchemes(p, Prayers.none).constant(Potions.none),
			monsters,
			sets,
			include_shared_xp=False,
			progress_callback=lambda i: self.optimize_panel.progressBar.setValue(i)
		)

		t1 = time.time()
		print(f"Solved in {t1-t0:.1f}s using {len(sets)} sets.")

		player = Player({})
		for slot, item_name in s.items():
			player.equip_by_name(item_name)
		stats = player.get_stats()

		tab = self.optimize_panel.best_in_slot_bonuses

		# tab.verticalHeaderItem(0).text().lower()
		tab.setItem(0, 0, QtWidgets.QTableWidgetItem(str(stats['attack_stab'])))
		tab.setItem(1, 0, QtWidgets.QTableWidgetItem(str(stats['attack_slash'])))
		tab.setItem(2, 0, QtWidgets.QTableWidgetItem(str(stats['attack_crush'])))
		tab.setItem(3, 0, QtWidgets.QTableWidgetItem(str(stats['attack_ranged'])))
		tab.setItem(4, 0, QtWidgets.QTableWidgetItem(str(stats['attack_magic'])))
		tab.setItem(5, 0, QtWidgets.QTableWidgetItem(str(stats['melee_strength'])))
		tab.setItem(6, 0, QtWidgets.QTableWidgetItem(str(stats['ranged_strength'])))
		tab.setItem(7, 0, QtWidgets.QTableWidgetItem(str(stats['magic_damage'])))
		tab.setItem(8, 0, QtWidgets.QTableWidgetItem(str(stats['attack_speed'])))
		tab.setItem(9, 0, QtWidgets.QTableWidgetItem(str("Not Supported")))

		slots = ['head', 'cape', 'neck', 'ammo', 'weapon', 'body', 'shield', 'legs', 'hands', 'feet', 'ring']
		for slot in slots:
			equipment_list = getattr(self.optimize_panel, slot)
			equipment_list.clear()
			if slot == 'weapon':
				equipment_list.addItem(s.get('weapon') if 'weapon' in s else s.get('2h'))
			else:
				equipment_list.addItem(s.get(slot))

		self.optimize_panel.xp_rate.setText(f"{xp/1000:,.1f}k")
		self.optimize_panel.attack_stance.setText(f"{stance}")

		# pp(sets)
		print(s, xp, stance)

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