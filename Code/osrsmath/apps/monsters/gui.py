from osrsmath.apps.GUI.monsters.monsters import Ui_Monsters
from PyQt5 import QtCore, QtGui, QtWidgets
import osrsmath.model.monsters as monsters
import webbrowser
from osrsmath.model.experience import combat_level

class GUI(Ui_Monsters):
	SEPERATOR = ' | '

	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)
		self.monster_data = monsters.get_monster_data()
		items = [f"{data['name'].lower()}{self.SEPERATOR}{ID}" for ID, data in self.monster_data.items()]
		completer = QtWidgets.QCompleter([i.lower() for i in items])

		self.search.addItems(items)
		self.search.setCompleter(completer)
		self.search.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
		self.search.textActivated.connect(self.on_select)
		self.xp_per_hit.setText('4')
		self.wiki_link.clicked.connect(self.open_wiki)

		self.on_select()

	def open_wiki(self):
		name, ID = self.search.currentText().split(self.SEPERATOR)
		monster = self.monster_data[ID]
		if ('wiki_url' in monster) and monster['wiki_url']:
			webbrowser.open(monster['wiki_url'])
		else:
			QtWidgets.QMessageBox(
				QtWidgets.QMessageBox.Info,
				'No wiki entry found.',
				f"{name} (id: {ID}) did not have a wiki url."
			).exec()


	def on_select(self):
		name, ID = self.search.currentText().split(self.SEPERATOR)
		monster = self.monster_data[ID]
		self.custom_name.setText(name)
		labels = [
			('health', 'hitpoints'),
			('attack', 'attack_level'),
			('strength', 'strength_level'),
			('defence', 'defence_level'),
			('ranged', 'ranged_level'),
			('magic', 'magic_level'),

			('aggressive_attack', 'attack_accuracy'),
			('aggressive_strength', 'melee_strength'),
			('aggressive_magic', 'attack_magic'),
			('aggressive_magic_damage', 'magic_damage'),
			('aggressive_ranged', 'attack_ranged'),
			('aggressive_ranged_strength', 'ranged_strength'),

			('defensive_stab', 'defence_stab'),
			('defensive_slash', 'defence_slash'),
			('defensive_crush', 'defence_crush'),
			('defensive_magic', 'defence_magic'),
			('defensive_ranged', 'defence_ranged'),
		]
		for attribute, key in labels:
			getattr(self, attribute).setText(str(monster[key]))
		self.combat_level.setText(str(combat_level({
			**{k.replace('_level', ''): v for k, v in self.get_monster().levels.items()},
			**{'prayer': 0}
		})))


	def get_monster(self):
		''' Returns a monster from the displayed data.
			@warning Only fills data for current use. Future work may need to
			    include other data. '''
		return monsters.Monster({
				'hitpoints': int(self.health.text()),
				'attack_level': int(self.attack.text()),
				'strength_level': int(self.strength.text()),
				'defence_level': int(self.defence.text()),
				'ranged_level': int(self.ranged.text()),
				'magic_level': int(self.magic.text()),
			}, {
				'defence_stab': int(self.defensive_stab.text()),
				'defence_slash': int(self.defensive_slash.text()),
				'defence_crush': int(self.defensive_crush.text()),
				'defence_magic': int(self.defensive_magic.text()),
				'defence_ranged': int(self.defensive_ranged.text()),
			},
			xp_per_damage=float(self.xp_per_hit.text())
		)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = GUI()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
