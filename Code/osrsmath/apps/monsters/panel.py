from osrsmath.apps.GUI.monsters.monsters_skeleton import Ui_Monsters
from PyQt5 import QtCore, QtGui, QtWidgets
import osrsmath.model.monsters as monsters
import webbrowser
from osrsmath.model.experience import combat_level
from pprint import pprint

NMZ_BOSSES = [
	"Trapped Soul",
	"Count Draynor",
	"Corsair Traitor",
	"Sand Snake",
	"Corrupt Lizardman",
	"King Roald",
	"Witch's experiment",
	"The Kendal",
	"Me",
	"Elvarg",
	"Moss Guardian",
	"Slagilith",
	"Nazastarool",
	"Treus Dayth",
	"Skeleton Hellhound",
	"Dagannoth mother",
	"Agrith-Naar",
	"Tree spirit",
	"Dad",
	"Tanglefoot",
	"Khazard warlord",
	"Arrg",
	"Black Knight Titan",
	"Ice Troll King",
	"Bouncer",
	"Glod",
	"Evil Chicken",
	"Agrith-Na-Na",
	"Flambeed",
	"Karamel",
	"Dessourt",
	"Gelatinnoth Mother",
	"Culinaromancer",
	"Chronozon",
	"Black demon",
	"Giant Roc",
	"Dessous",
	"Damis",
	"Fareed",
	"Kamil",
	"Nezikchened",
	"Barrelchest",
	"Giant scarab",
	"Jungle Demon",
	"Elven traitor",
	"Essyllt",	"The Untouchable",
	"The Everlasting",
	"The Inadequacy",
]

class MonsterPanel(QtWidgets.QWidget, Ui_Monsters):
	SEPERATOR = ' | '

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.monster_data = monsters.get_monster_data()

		self.search.textActivated.connect(self.on_select)
		self.nmz_only.stateChanged.connect(self.nmz_only_changed)
		self.xp_per_hit.setText('4')
		self.wiki_link.clicked.connect(self.open_wiki)

		self.nmz_only_changed()
		self.on_select()

	def nmz_only_changed(self):
		if self.nmz_only.isChecked():
			opponents = []
			for item_id, data in self.monster_data.items():
				if any(name.lower() in data['name'].lower() for name in NMZ_BOSSES):
					opponents.append((data['id'], {'name': data['name']}))
		else:
			opponents = self.monster_data.items()
		items = [f"{data['name'].lower()}{self.SEPERATOR}{ID}" for ID, data in opponents]

		self.search.clear()
		completer = QtWidgets.QCompleter([i.lower() for i in items])
		self.search.addItems(items)
		self.search.setCompleter(completer)
		self.search.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
		self.on_select()

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

	def get_monster(self):
		''' Returns a monster from the displayed data.
			@warning Only fills data for current use. Future work may need to
			    include other data. '''
		return monsters.Monster(**self.get_monster_as_dict())

	def get_monster_as_dict(self):
		return {
			'levels': {
				'hitpoints': int(self.health.text()),
				'attack': int(self.attack.text()),
				'strength': int(self.strength.text()),
				'defence': int(self.defence.text()),
				'ranged': int(self.ranged.text()),
				'magic': int(self.magic.text()),
			},
			'stats': {
				'defence_stab': int(self.defensive_stab.text()),
				'defence_slash': int(self.defensive_slash.text()),
				'defence_crush': int(self.defensive_crush.text()),
				'defence_magic': int(self.defensive_magic.text()),
				'defence_ranged': int(self.defensive_ranged.text()),
			},
			'xp_per_damage': float(self.xp_per_hit.text()),
		}