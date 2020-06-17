# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'player_skeleton.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(285, 252)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_thieving = QLabel(Form)
        self.label_thieving.setObjectName(u"label_thieving")
        self.label_thieving.setPixmap(QPixmap(u":/skill_icons/Thieving.png"))
        self.label_thieving.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_thieving, 4, 2, 1, 1)

        self.combat_level = QLineEdit(Form)
        self.combat_level.setObjectName(u"combat_level")
        self.combat_level.setEnabled(False)
        self.combat_level.setMinimumSize(QSize(54, 0))
        self.combat_level.setMaxLength(3)

        self.gridLayout.addWidget(self.combat_level, 8, 5, 1, 1)

        self.label_farming = QLabel(Form)
        self.label_farming.setObjectName(u"label_farming")
        self.label_farming.setPixmap(QPixmap(u":/skill_icons/Farming.png"))
        self.label_farming.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_farming, 7, 4, 1, 1)

        self.slayer = QLineEdit(Form)
        self.slayer.setObjectName(u"slayer")
        self.slayer.setMinimumSize(QSize(54, 0))
        self.slayer.setMaxLength(2)

        self.gridLayout.addWidget(self.slayer, 7, 3, 1, 1)

        self.smithing = QLineEdit(Form)
        self.smithing.setObjectName(u"smithing")
        self.smithing.setMinimumSize(QSize(54, 0))
        self.smithing.setMaxLength(2)

        self.gridLayout.addWidget(self.smithing, 2, 5, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u":/monster/Combat_icon.webp"))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 8, 4, 1, 1)

        self.fishing = QLineEdit(Form)
        self.fishing.setObjectName(u"fishing")
        self.fishing.setMinimumSize(QSize(54, 0))
        self.fishing.setMaxLength(2)

        self.gridLayout.addWidget(self.fishing, 3, 5, 1, 1)

        self.prayer = QLineEdit(Form)
        self.prayer.setObjectName(u"prayer")
        self.prayer.setMinimumSize(QSize(54, 0))
        self.prayer.setMaxLength(2)

        self.gridLayout.addWidget(self.prayer, 5, 1, 1, 1)

        self.farming = QLineEdit(Form)
        self.farming.setObjectName(u"farming")
        self.farming.setMinimumSize(QSize(54, 0))
        self.farming.setMaxLength(2)

        self.gridLayout.addWidget(self.farming, 7, 5, 1, 1)

        self.magic = QLineEdit(Form)
        self.magic.setObjectName(u"magic")
        self.magic.setMinimumSize(QSize(54, 0))
        self.magic.setMaxLength(2)

        self.gridLayout.addWidget(self.magic, 6, 1, 1, 1)

        self.label_hunter = QLabel(Form)
        self.label_hunter.setObjectName(u"label_hunter")
        self.label_hunter.setPixmap(QPixmap(u":/skill_icons/Hunter.png"))
        self.label_hunter.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_hunter, 8, 2, 1, 1)

        self.label_prayer = QLabel(Form)
        self.label_prayer.setObjectName(u"label_prayer")
        self.label_prayer.setPixmap(QPixmap(u":/skill_icons/Prayer.png"))
        self.label_prayer.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_prayer, 5, 0, 1, 1)

        self.defence = QLineEdit(Form)
        self.defence.setObjectName(u"defence")
        self.defence.setMinimumSize(QSize(54, 0))
        self.defence.setMaxLength(2)

        self.gridLayout.addWidget(self.defence, 3, 1, 1, 1)

        self.runecraft = QLineEdit(Form)
        self.runecraft.setObjectName(u"runecraft")
        self.runecraft.setMinimumSize(QSize(54, 0))
        self.runecraft.setMaxLength(2)

        self.gridLayout.addWidget(self.runecraft, 7, 1, 1, 1)

        self.label_hitpoints = QLabel(Form)
        self.label_hitpoints.setObjectName(u"label_hitpoints")
        self.label_hitpoints.setPixmap(QPixmap(u":/skill_icons/Hitpoints.png"))
        self.label_hitpoints.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_hitpoints, 1, 2, 1, 1)

        self.hitpoints = QLineEdit(Form)
        self.hitpoints.setObjectName(u"hitpoints")
        self.hitpoints.setMinimumSize(QSize(54, 0))
        self.hitpoints.setMaxLength(2)

        self.gridLayout.addWidget(self.hitpoints, 1, 3, 1, 1)

        self.label_woodcutting = QLabel(Form)
        self.label_woodcutting.setObjectName(u"label_woodcutting")
        self.label_woodcutting.setPixmap(QPixmap(u":/skill_icons/Woodcutting.png"))
        self.label_woodcutting.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_woodcutting, 6, 4, 1, 1)

        self.mining = QLineEdit(Form)
        self.mining.setObjectName(u"mining")
        self.mining.setMinimumSize(QSize(54, 0))
        self.mining.setMaxLength(2)

        self.gridLayout.addWidget(self.mining, 1, 5, 1, 1)

        self.label_fletching = QLabel(Form)
        self.label_fletching.setObjectName(u"label_fletching")
        self.label_fletching.setPixmap(QPixmap(u":/skill_icons/Fletching.png"))
        self.label_fletching.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_fletching, 6, 2, 1, 1)

        self.label_defence = QLabel(Form)
        self.label_defence.setObjectName(u"label_defence")
        self.label_defence.setPixmap(QPixmap(u":/skill_icons/Defence.png"))
        self.label_defence.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_defence, 3, 0, 1, 1)

        self.label_crafting = QLabel(Form)
        self.label_crafting.setObjectName(u"label_crafting")
        self.label_crafting.setPixmap(QPixmap(u":/skill_icons/Crafting.png"))
        self.label_crafting.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_crafting, 5, 2, 1, 1)

        self.firemaking = QLineEdit(Form)
        self.firemaking.setObjectName(u"firemaking")
        self.firemaking.setMinimumSize(QSize(54, 0))
        self.firemaking.setMaxLength(2)

        self.gridLayout.addWidget(self.firemaking, 5, 5, 1, 1)

        self.agility = QLineEdit(Form)
        self.agility.setObjectName(u"agility")
        self.agility.setMinimumSize(QSize(54, 0))
        self.agility.setMaxLength(2)

        self.gridLayout.addWidget(self.agility, 2, 3, 1, 1)

        self.ranged = QLineEdit(Form)
        self.ranged.setObjectName(u"ranged")
        self.ranged.setMinimumSize(QSize(54, 0))
        self.ranged.setMaxLength(2)

        self.gridLayout.addWidget(self.ranged, 4, 1, 1, 1)

        self.label_agility = QLabel(Form)
        self.label_agility.setObjectName(u"label_agility")
        self.label_agility.setPixmap(QPixmap(u":/skill_icons/Agility.png"))
        self.label_agility.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_agility, 2, 2, 1, 1)

        self.attack = QLineEdit(Form)
        self.attack.setObjectName(u"attack")
        self.attack.setMinimumSize(QSize(54, 0))
        self.attack.setMaxLength(2)
        self.attack.setCursorMoveStyle(Qt.LogicalMoveStyle)

        self.gridLayout.addWidget(self.attack, 1, 1, 1, 1)

        self.fletching = QLineEdit(Form)
        self.fletching.setObjectName(u"fletching")
        self.fletching.setMinimumSize(QSize(54, 0))
        self.fletching.setMaxLength(2)

        self.gridLayout.addWidget(self.fletching, 6, 3, 1, 1)

        self.label_construction = QLabel(Form)
        self.label_construction.setObjectName(u"label_construction")
        self.label_construction.setPixmap(QPixmap(u":/skill_icons/Construction.png"))
        self.label_construction.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_construction, 8, 0, 1, 1)

        self.woodcutting = QLineEdit(Form)
        self.woodcutting.setObjectName(u"woodcutting")
        self.woodcutting.setMinimumSize(QSize(54, 0))
        self.woodcutting.setMaxLength(2)

        self.gridLayout.addWidget(self.woodcutting, 6, 5, 1, 1)

        self.construction = QLineEdit(Form)
        self.construction.setObjectName(u"construction")
        self.construction.setMinimumSize(QSize(54, 0))
        self.construction.setMaxLength(2)

        self.gridLayout.addWidget(self.construction, 8, 1, 1, 1)

        self.strength = QLineEdit(Form)
        self.strength.setObjectName(u"strength")
        self.strength.setMinimumSize(QSize(54, 0))
        self.strength.setMaxLength(2)

        self.gridLayout.addWidget(self.strength, 2, 1, 1, 1)

        self.label_magic = QLabel(Form)
        self.label_magic.setObjectName(u"label_magic")
        self.label_magic.setPixmap(QPixmap(u":/skill_icons/Magic.png"))
        self.label_magic.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_magic, 6, 0, 1, 1)

        self.label_ranged = QLabel(Form)
        self.label_ranged.setObjectName(u"label_ranged")
        self.label_ranged.setPixmap(QPixmap(u":/skill_icons/Ranged.png"))
        self.label_ranged.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_ranged, 4, 0, 1, 1)

        self.label_attack = QLabel(Form)
        self.label_attack.setObjectName(u"label_attack")
        self.label_attack.setPixmap(QPixmap(u":/skill_icons/Attack.png"))
        self.label_attack.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_attack, 1, 0, 1, 1)

        self.label_slayer = QLabel(Form)
        self.label_slayer.setObjectName(u"label_slayer")
        self.label_slayer.setPixmap(QPixmap(u":/skill_icons/Slayer.png"))
        self.label_slayer.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_slayer, 7, 2, 1, 1)

        self.label_mining = QLabel(Form)
        self.label_mining.setObjectName(u"label_mining")
        self.label_mining.setPixmap(QPixmap(u":/skill_icons/Mining.png"))
        self.label_mining.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_mining, 1, 4, 1, 1)

        self.label_smithing = QLabel(Form)
        self.label_smithing.setObjectName(u"label_smithing")
        self.label_smithing.setPixmap(QPixmap(u":/skill_icons/Smithing.png"))
        self.label_smithing.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_smithing, 2, 4, 1, 1)

        self.thieving = QLineEdit(Form)
        self.thieving.setObjectName(u"thieving")
        self.thieving.setMinimumSize(QSize(54, 0))
        self.thieving.setMaxLength(2)

        self.gridLayout.addWidget(self.thieving, 4, 3, 1, 1)

        self.label_runecraft = QLabel(Form)
        self.label_runecraft.setObjectName(u"label_runecraft")
        self.label_runecraft.setPixmap(QPixmap(u":/skill_icons/Runecraft.png"))
        self.label_runecraft.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_runecraft, 7, 0, 1, 1)

        self.hunter = QLineEdit(Form)
        self.hunter.setObjectName(u"hunter")
        self.hunter.setMinimumSize(QSize(54, 0))
        self.hunter.setMaxLength(2)

        self.gridLayout.addWidget(self.hunter, 8, 3, 1, 1)

        self.label_herblore = QLabel(Form)
        self.label_herblore.setObjectName(u"label_herblore")
        self.label_herblore.setPixmap(QPixmap(u":/skill_icons/Herblore.png"))
        self.label_herblore.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_herblore, 3, 2, 1, 1)

        self.label_fishing = QLabel(Form)
        self.label_fishing.setObjectName(u"label_fishing")
        self.label_fishing.setPixmap(QPixmap(u":/skill_icons/Fishing.png"))
        self.label_fishing.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_fishing, 3, 4, 1, 1)

        self.label_firemaking = QLabel(Form)
        self.label_firemaking.setObjectName(u"label_firemaking")
        self.label_firemaking.setPixmap(QPixmap(u":/skill_icons/Firemaking.png"))
        self.label_firemaking.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_firemaking, 5, 4, 1, 1)

        self.label_strength = QLabel(Form)
        self.label_strength.setObjectName(u"label_strength")
        self.label_strength.setPixmap(QPixmap(u":/skill_icons/Strength.png"))
        self.label_strength.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_strength, 2, 0, 1, 1)

        self.herblore = QLineEdit(Form)
        self.herblore.setObjectName(u"herblore")
        self.herblore.setMinimumSize(QSize(54, 0))
        self.herblore.setMaxLength(2)

        self.gridLayout.addWidget(self.herblore, 3, 3, 1, 1)

        self.label_cooking = QLabel(Form)
        self.label_cooking.setObjectName(u"label_cooking")
        self.label_cooking.setPixmap(QPixmap(u":/skill_icons/Cooking.png"))
        self.label_cooking.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_cooking, 4, 4, 1, 1)

        self.crafting = QLineEdit(Form)
        self.crafting.setObjectName(u"crafting")
        self.crafting.setMinimumSize(QSize(54, 0))
        self.crafting.setMaxLength(2)

        self.gridLayout.addWidget(self.crafting, 5, 3, 1, 1)

        self.cooking = QLineEdit(Form)
        self.cooking.setObjectName(u"cooking")
        self.cooking.setMinimumSize(QSize(54, 0))
        self.cooking.setMaxLength(2)

        self.gridLayout.addWidget(self.cooking, 4, 5, 1, 1)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)

        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 4)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 2)

        self.label_thieving.raise_()
        self.label_attack.raise_()
        self.label_crafting.raise_()
        self.label_slayer.raise_()
        self.label_agility.raise_()
        self.label_farming.raise_()
        self.label_runecraft.raise_()
        self.label_woodcutting.raise_()
        self.label_hunter.raise_()
        self.label_herblore.raise_()
        self.label_mining.raise_()
        self.label_construction.raise_()
        self.label_defence.raise_()
        self.label_magic.raise_()
        self.label_prayer.raise_()
        self.label_hitpoints.raise_()
        self.label_smithing.raise_()
        self.label_strength.raise_()
        self.label_firemaking.raise_()
        self.label_ranged.raise_()
        self.label_fletching.raise_()
        self.label_cooking.raise_()
        self.label_fishing.raise_()
        self.label.raise_()
        self.hitpoints.raise_()
        self.agility.raise_()
        self.herblore.raise_()
        self.thieving.raise_()
        self.crafting.raise_()
        self.fletching.raise_()
        self.slayer.raise_()
        self.hunter.raise_()
        self.mining.raise_()
        self.smithing.raise_()
        self.fishing.raise_()
        self.cooking.raise_()
        self.firemaking.raise_()
        self.woodcutting.raise_()
        self.farming.raise_()
        self.combat_level.raise_()
        self.construction.raise_()
        self.runecraft.raise_()
        self.magic.raise_()
        self.attack.raise_()
        self.strength.raise_()
        self.defence.raise_()
        self.ranged.raise_()
        self.prayer.raise_()
        self.lineEdit.raise_()
        self.label_2.raise_()
        QWidget.setTabOrder(self.attack, self.strength)
        QWidget.setTabOrder(self.strength, self.defence)
        QWidget.setTabOrder(self.defence, self.ranged)
        QWidget.setTabOrder(self.ranged, self.prayer)
        QWidget.setTabOrder(self.prayer, self.magic)
        QWidget.setTabOrder(self.magic, self.runecraft)
        QWidget.setTabOrder(self.runecraft, self.construction)
        QWidget.setTabOrder(self.construction, self.hitpoints)
        QWidget.setTabOrder(self.hitpoints, self.agility)
        QWidget.setTabOrder(self.agility, self.herblore)
        QWidget.setTabOrder(self.herblore, self.thieving)
        QWidget.setTabOrder(self.thieving, self.crafting)
        QWidget.setTabOrder(self.crafting, self.fletching)
        QWidget.setTabOrder(self.fletching, self.slayer)
        QWidget.setTabOrder(self.slayer, self.hunter)
        QWidget.setTabOrder(self.hunter, self.mining)
        QWidget.setTabOrder(self.mining, self.smithing)
        QWidget.setTabOrder(self.smithing, self.fishing)
        QWidget.setTabOrder(self.fishing, self.cooking)
        QWidget.setTabOrder(self.cooking, self.firemaking)
        QWidget.setTabOrder(self.firemaking, self.woodcutting)
        QWidget.setTabOrder(self.woodcutting, self.farming)
        QWidget.setTabOrder(self.farming, self.combat_level)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_thieving.setText("")
        self.combat_level.setText("")
        self.label_farming.setText("")
        self.smithing.setText("")
        self.label.setText("")
        self.fishing.setText("")
        self.farming.setText("")
        self.label_hunter.setText("")
        self.label_prayer.setText("")
        self.label_hitpoints.setText("")
        self.label_woodcutting.setText("")
        self.mining.setText("")
        self.label_fletching.setText("")
        self.label_defence.setText("")
        self.label_crafting.setText("")
        self.firemaking.setText("")
        self.label_agility.setText("")
        self.attack.setText("")
        self.label_construction.setText("")
        self.woodcutting.setText("")
        self.label_magic.setText("")
        self.label_ranged.setText("")
        self.label_attack.setText("")
        self.label_slayer.setText("")
        self.label_mining.setText("")
        self.label_smithing.setText("")
        self.label_runecraft.setText("")
        self.label_herblore.setText("")
        self.label_fishing.setText("")
        self.label_firemaking.setText("")
        self.label_strength.setText("")
        self.label_cooking.setText("")
        self.cooking.setText("")
        self.lineEdit.setText(QCoreApplication.translate("Form", u"Lookup Not Yet Supported", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Username:", None))
    # retranslateUi

