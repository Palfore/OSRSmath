# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player_stats.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(538, 252)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_thieving = QtWidgets.QLabel(Form)
        self.label_thieving.setText("")
        self.label_thieving.setPixmap(QtGui.QPixmap("../images/skill_icons/Thieving.png"))
        self.label_thieving.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_thieving.setObjectName("label_thieving")
        self.gridLayout.addWidget(self.label_thieving, 3, 2, 1, 1)
        self.thieving = QtWidgets.QLineEdit(Form)
        self.thieving.setObjectName("thieving")
        self.gridLayout.addWidget(self.thieving, 3, 3, 1, 1)
        self.label_attack = QtWidgets.QLabel(Form)
        self.label_attack.setText("")
        self.label_attack.setPixmap(QtGui.QPixmap("../images/skill_icons/Attack.png"))
        self.label_attack.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_attack.setObjectName("label_attack")
        self.gridLayout.addWidget(self.label_attack, 0, 0, 1, 1)
        self.label_crafting = QtWidgets.QLabel(Form)
        self.label_crafting.setText("")
        self.label_crafting.setPixmap(QtGui.QPixmap("../images/skill_icons/Crafting.png"))
        self.label_crafting.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_crafting.setObjectName("label_crafting")
        self.gridLayout.addWidget(self.label_crafting, 4, 2, 1, 1)
        self.ranged = QtWidgets.QLineEdit(Form)
        self.ranged.setObjectName("ranged")
        self.gridLayout.addWidget(self.ranged, 3, 1, 1, 1)
        self.magic = QtWidgets.QLineEdit(Form)
        self.magic.setObjectName("magic")
        self.gridLayout.addWidget(self.magic, 5, 1, 1, 1)
        self.firemaking = QtWidgets.QLineEdit(Form)
        self.firemaking.setObjectName("firemaking")
        self.gridLayout.addWidget(self.firemaking, 4, 5, 1, 1)
        self.slayer = QtWidgets.QLineEdit(Form)
        self.slayer.setObjectName("slayer")
        self.gridLayout.addWidget(self.slayer, 6, 3, 1, 1)
        self.farming = QtWidgets.QLineEdit(Form)
        self.farming.setObjectName("farming")
        self.gridLayout.addWidget(self.farming, 6, 5, 1, 1)
        self.label_slayer = QtWidgets.QLabel(Form)
        self.label_slayer.setText("")
        self.label_slayer.setPixmap(QtGui.QPixmap("../images/skill_icons/Slayer.png"))
        self.label_slayer.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_slayer.setObjectName("label_slayer")
        self.gridLayout.addWidget(self.label_slayer, 6, 2, 1, 1)
        self.label_agility = QtWidgets.QLabel(Form)
        self.label_agility.setText("")
        self.label_agility.setPixmap(QtGui.QPixmap("../images/skill_icons/Agility.png"))
        self.label_agility.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_agility.setObjectName("label_agility")
        self.gridLayout.addWidget(self.label_agility, 1, 2, 1, 1)
        self.label_farming = QtWidgets.QLabel(Form)
        self.label_farming.setText("")
        self.label_farming.setPixmap(QtGui.QPixmap("../images/skill_icons/Farming.png"))
        self.label_farming.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_farming.setObjectName("label_farming")
        self.gridLayout.addWidget(self.label_farming, 6, 4, 1, 1)
        self.prayer = QtWidgets.QLineEdit(Form)
        self.prayer.setObjectName("prayer")
        self.gridLayout.addWidget(self.prayer, 4, 1, 1, 1)
        self.runecraft = QtWidgets.QLineEdit(Form)
        self.runecraft.setObjectName("runecraft")
        self.gridLayout.addWidget(self.runecraft, 6, 1, 1, 1)
        self.strength = QtWidgets.QLineEdit(Form)
        self.strength.setObjectName("strength")
        self.gridLayout.addWidget(self.strength, 1, 1, 1, 1)
        self.herblore = QtWidgets.QLineEdit(Form)
        self.herblore.setObjectName("herblore")
        self.gridLayout.addWidget(self.herblore, 2, 3, 1, 1)
        self.label_runecraft = QtWidgets.QLabel(Form)
        self.label_runecraft.setText("")
        self.label_runecraft.setPixmap(QtGui.QPixmap("../images/skill_icons/Runecraft.png"))
        self.label_runecraft.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_runecraft.setObjectName("label_runecraft")
        self.gridLayout.addWidget(self.label_runecraft, 6, 0, 1, 1)
        self.cooking = QtWidgets.QLineEdit(Form)
        self.cooking.setObjectName("cooking")
        self.gridLayout.addWidget(self.cooking, 3, 5, 1, 1)
        self.agility = QtWidgets.QLineEdit(Form)
        self.agility.setObjectName("agility")
        self.gridLayout.addWidget(self.agility, 1, 3, 1, 1)
        self.label_woodcutting = QtWidgets.QLabel(Form)
        self.label_woodcutting.setText("")
        self.label_woodcutting.setPixmap(QtGui.QPixmap("../images/skill_icons/Woodcutting.png"))
        self.label_woodcutting.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_woodcutting.setObjectName("label_woodcutting")
        self.gridLayout.addWidget(self.label_woodcutting, 5, 4, 1, 1)
        self.attack = QtWidgets.QLineEdit(Form)
        self.attack.setObjectName("attack")
        self.gridLayout.addWidget(self.attack, 0, 1, 1, 1)
        self.mining = QtWidgets.QLineEdit(Form)
        self.mining.setObjectName("mining")
        self.gridLayout.addWidget(self.mining, 0, 5, 1, 1)
        self.defence = QtWidgets.QLineEdit(Form)
        self.defence.setObjectName("defence")
        self.gridLayout.addWidget(self.defence, 2, 1, 1, 1)
        self.crafting = QtWidgets.QLineEdit(Form)
        self.crafting.setObjectName("crafting")
        self.gridLayout.addWidget(self.crafting, 4, 3, 1, 1)
        self.label_hunter = QtWidgets.QLabel(Form)
        self.label_hunter.setText("")
        self.label_hunter.setPixmap(QtGui.QPixmap("../images/skill_icons/Hunter.png"))
        self.label_hunter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_hunter.setObjectName("label_hunter")
        self.gridLayout.addWidget(self.label_hunter, 7, 2, 1, 1)
        self.construction = QtWidgets.QLineEdit(Form)
        self.construction.setObjectName("construction")
        self.gridLayout.addWidget(self.construction, 7, 1, 1, 1)
        self.smithing = QtWidgets.QLineEdit(Form)
        self.smithing.setObjectName("smithing")
        self.gridLayout.addWidget(self.smithing, 1, 5, 1, 1)
        self.hitpoints = QtWidgets.QLineEdit(Form)
        self.hitpoints.setObjectName("hitpoints")
        self.gridLayout.addWidget(self.hitpoints, 0, 3, 1, 1)
        self.label_herblore = QtWidgets.QLabel(Form)
        self.label_herblore.setText("")
        self.label_herblore.setPixmap(QtGui.QPixmap("../images/skill_icons/Herblore.png"))
        self.label_herblore.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_herblore.setObjectName("label_herblore")
        self.gridLayout.addWidget(self.label_herblore, 2, 2, 1, 1)
        self.label_mining = QtWidgets.QLabel(Form)
        self.label_mining.setText("")
        self.label_mining.setPixmap(QtGui.QPixmap("../images/skill_icons/Mining.png"))
        self.label_mining.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_mining.setObjectName("label_mining")
        self.gridLayout.addWidget(self.label_mining, 0, 4, 1, 1)
        self.hunter = QtWidgets.QLineEdit(Form)
        self.hunter.setObjectName("hunter")
        self.gridLayout.addWidget(self.hunter, 7, 3, 1, 1)
        self.label_construction = QtWidgets.QLabel(Form)
        self.label_construction.setText("")
        self.label_construction.setPixmap(QtGui.QPixmap("../images/skill_icons/Construction.png"))
        self.label_construction.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_construction.setObjectName("label_construction")
        self.gridLayout.addWidget(self.label_construction, 7, 0, 1, 1)
        self.label_defence = QtWidgets.QLabel(Form)
        self.label_defence.setText("")
        self.label_defence.setPixmap(QtGui.QPixmap("../images/skill_icons/Defence.png"))
        self.label_defence.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_defence.setObjectName("label_defence")
        self.gridLayout.addWidget(self.label_defence, 2, 0, 1, 1)
        self.label_magic = QtWidgets.QLabel(Form)
        self.label_magic.setText("")
        self.label_magic.setPixmap(QtGui.QPixmap("../images/skill_icons/Magic.png"))
        self.label_magic.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_magic.setObjectName("label_magic")
        self.gridLayout.addWidget(self.label_magic, 5, 0, 1, 1)
        self.label_prayer = QtWidgets.QLabel(Form)
        self.label_prayer.setText("")
        self.label_prayer.setPixmap(QtGui.QPixmap("../images/skill_icons/Prayer.png"))
        self.label_prayer.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_prayer.setObjectName("label_prayer")
        self.gridLayout.addWidget(self.label_prayer, 4, 0, 1, 1)
        self.label_hitpoints = QtWidgets.QLabel(Form)
        self.label_hitpoints.setText("")
        self.label_hitpoints.setPixmap(QtGui.QPixmap("../images/skill_icons/Hitpoints.png"))
        self.label_hitpoints.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_hitpoints.setObjectName("label_hitpoints")
        self.gridLayout.addWidget(self.label_hitpoints, 0, 2, 1, 1)
        self.fishing = QtWidgets.QLineEdit(Form)
        self.fishing.setObjectName("fishing")
        self.gridLayout.addWidget(self.fishing, 2, 5, 1, 1)
        self.fletching = QtWidgets.QLineEdit(Form)
        self.fletching.setObjectName("fletching")
        self.gridLayout.addWidget(self.fletching, 5, 3, 1, 1)
        self.woodcutting = QtWidgets.QLineEdit(Form)
        self.woodcutting.setObjectName("woodcutting")
        self.gridLayout.addWidget(self.woodcutting, 5, 5, 1, 1)
        self.label_smithing = QtWidgets.QLabel(Form)
        self.label_smithing.setText("")
        self.label_smithing.setPixmap(QtGui.QPixmap("../images/skill_icons/Smithing.png"))
        self.label_smithing.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_smithing.setObjectName("label_smithing")
        self.gridLayout.addWidget(self.label_smithing, 1, 4, 1, 1)
        self.label_strength = QtWidgets.QLabel(Form)
        self.label_strength.setText("")
        self.label_strength.setPixmap(QtGui.QPixmap("../images/skill_icons/Strength.png"))
        self.label_strength.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_strength.setObjectName("label_strength")
        self.gridLayout.addWidget(self.label_strength, 1, 0, 1, 1)
        self.label_firemaking = QtWidgets.QLabel(Form)
        self.label_firemaking.setText("")
        self.label_firemaking.setPixmap(QtGui.QPixmap("../images/skill_icons/Firemaking.png"))
        self.label_firemaking.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_firemaking.setObjectName("label_firemaking")
        self.gridLayout.addWidget(self.label_firemaking, 4, 4, 1, 1)
        self.label_ranged = QtWidgets.QLabel(Form)
        self.label_ranged.setText("")
        self.label_ranged.setPixmap(QtGui.QPixmap("../images/skill_icons/Ranged.png"))
        self.label_ranged.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_ranged.setObjectName("label_ranged")
        self.gridLayout.addWidget(self.label_ranged, 3, 0, 1, 1)
        self.label_fletching = QtWidgets.QLabel(Form)
        self.label_fletching.setText("")
        self.label_fletching.setPixmap(QtGui.QPixmap("../images/skill_icons/Fletching.png"))
        self.label_fletching.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_fletching.setObjectName("label_fletching")
        self.gridLayout.addWidget(self.label_fletching, 5, 2, 1, 1)
        self.label_cooking = QtWidgets.QLabel(Form)
        self.label_cooking.setText("")
        self.label_cooking.setPixmap(QtGui.QPixmap("../images/skill_icons/Cooking.png"))
        self.label_cooking.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_cooking.setObjectName("label_cooking")
        self.gridLayout.addWidget(self.label_cooking, 3, 4, 1, 1)
        self.label_fishing = QtWidgets.QLabel(Form)
        self.label_fishing.setText("")
        self.label_fishing.setPixmap(QtGui.QPixmap("../images/skill_icons/Fishing.png"))
        self.label_fishing.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_fishing.setObjectName("label_fishing")
        self.gridLayout.addWidget(self.label_fishing, 2, 4, 1, 1)
        self.combat_level = QtWidgets.QLineEdit(Form)
        self.combat_level.setEnabled(False)
        self.combat_level.setObjectName("combat_level")
        self.gridLayout.addWidget(self.combat_level, 7, 5, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../images/monster/Combat_icon.webp"))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 7, 4, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
