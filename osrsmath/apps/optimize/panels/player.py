from osrsmath.apps.GUI.optimize.player_skeleton import Ui_Form
from osrsmath.apps.GUI.shared.widgets import Savable
from osrsmath.general.skills import get_skills, get_combat_skills
from osrsmath.combat.experience import combat_level
from PySide2 import QtCore, QtGui, QtWidgets

class PlayerPanel(QtWidgets.QWidget, Ui_Form, Savable):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.entities = {
			skill: Savable.Entity(
				getattr(self, skill),
				'',
				lambda o, v: o.setText(v),
				lambda o: o.text()
			) for skill in get_skills(lower=True)
		}
		self.entities['cmb'] = Savable.Entity(
			self.combat_level, '', lambda o, v: o.setText(v), lambda o: o.text()
		)

		# Only integer input allowed for skill levels
		for skill in get_skills(lower=True):
			self.entities[skill].object.setValidator(QtGui.QIntValidator(1, 99))

		for skill in get_combat_skills(lower=True):
			self.entities[skill].object.editingFinished.connect(self.update_cmb_level)

	def update_cmb_level(self):
		try:
			self.entities['cmb'].set(str(combat_level(self.get_stats())))
		except ValueError as e:
			print(e)
			pass


	def get_stats(self):
		''' Returns a dictionary of all displayed levels (including cmb). '''
		return {
			skill: int(self.entities[skill].get()) for skill in get_skills(lower=True) + ['cmb'] if self.entities[skill].get() != ''
		}