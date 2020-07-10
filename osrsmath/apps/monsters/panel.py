from osrsmath.apps.GUI.monsters.monsters_skeleton import Ui_Monsters
from PySide2 import QtCore, QtGui, QtWidgets
import osrsmath.combat.monsters as monsters
import webbrowser
from osrsmath.combat.experience import combat_level
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
	LABELS = [
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
	ADD_TOOLTIP = "Reduce the search to only contain nmz boss names."
	NMZ_ONLY_TOOLTIP = "Add this monster to your monster pool."

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.monster_data = monsters.get_monster_data()

		self.search.textActivated.connect(self.on_select)
		self.nmz_only.stateChanged.connect(self.nmz_only_changed)
		self.xp_per_hit.setText('4')
		self.wiki_link.clicked.connect(self.open_wiki)
		for label, obj in self.LABELS:
			getattr(self, label).setValidator(QtGui.QIntValidator())

		self.nmz_only_changed()
		self.on_select()


		self.nmz_only.setToolTip(self.ADD_TOOLTIP)
		self.add.setToolTip(self.NMZ_ONLY_TOOLTIP)

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
		for attribute, key in self.LABELS:
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
			).exec_()

	def get_monster(self):
		''' Returns a monster from the displayed data.
			@warning Only fills data for current use. Future work may need to
			    include other data. '''
		return monsters.Monster(**self.get_monster_as_dict())

	def get_monster_as_dict(self):
		extract = lambda x: int(x.text() if x.text().strip() != '' else 0)
		return {
			'levels': {
				'hitpoints': extract(self.health),
				'attack': extract(self.attack),
				'strength': extract(self.strength),
				'defence': extract(self.defence),
				'ranged': extract(self.ranged),
				'magic': extract(self.magic),
			},
			'stats': {
				'defence_stab': extract(self.defensive_stab),
				'defence_slash': extract(self.defensive_slash),
				'defence_crush': extract(self.defensive_crush),
				'defence_magic': extract(self.defensive_magic),
				'defence_ranged': extract(self.defensive_ranged),
			},
			'xp_per_damage': float(self.xp_per_hit.text()),
		}

	def fill_monster(self, name, monster: dict):
		extract = lambda x: str(int(x))
		self.search.clear()
		self.custom_name.setText(name)
		self.health.setText(extract(monster['levels']['hitpoints']))
		self.attack.setText(extract(monster['levels']['attack']))
		self.strength.setText(extract(monster['levels']['strength']))
		self.defence.setText(extract(monster['levels']['defence']))
		self.ranged.setText(extract(monster['levels']['ranged']))
		self.magic.setText(extract(monster['levels']['magic']))

		self.defensive_stab.setText(extract(monster['stats']['defence_stab']))
		self.defensive_slash.setText(extract(monster['stats']['defence_slash']))
		self.defensive_crush.setText(extract(monster['stats']['defence_crush']))
		self.defensive_magic.setText(extract(monster['stats']['defence_magic']))
		self.defensive_ranged.setText(extract(monster['stats']['defence_ranged']))

		self.xp_per_hit.setText(str(monster['xp_per_damage']))



