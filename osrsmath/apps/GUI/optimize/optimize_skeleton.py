# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'optimize_skeleton.ui'
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
        Form.resize(714, 738)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.below_skill = QComboBox(Form)
        self.below_skill.addItem("")
        self.below_skill.addItem("")
        self.below_skill.addItem("")
        self.below_skill.setObjectName(u"below_skill")

        self.gridLayout.addWidget(self.below_skill, 7, 1, 1, 4)

        self.potion_attributes = QComboBox(Form)
        self.potion_attributes.addItem("")
        self.potion_attributes.addItem("")
        self.potion_attributes.addItem("")
        self.potion_attributes.setObjectName(u"potion_attributes")

        self.gridLayout.addWidget(self.potion_attributes, 5, 5, 1, 3)

        self.best_in_slot_bonuses = QTableWidget(Form)
        if (self.best_in_slot_bonuses.columnCount() < 1):
            self.best_in_slot_bonuses.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.best_in_slot_bonuses.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.best_in_slot_bonuses.rowCount() < 10):
            self.best_in_slot_bonuses.setRowCount(10)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(2, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(3, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(4, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(5, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(6, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(7, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(8, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(9, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(0, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(1, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(2, 0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(3, 0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(4, 0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(5, 0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(6, 0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(7, 0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(8, 0, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.best_in_slot_bonuses.setItem(9, 0, __qtablewidgetitem20)
        self.best_in_slot_bonuses.setObjectName(u"best_in_slot_bonuses")
        self.best_in_slot_bonuses.setShowGrid(True)
        self.best_in_slot_bonuses.horizontalHeader().setStretchLastSection(True)
        self.best_in_slot_bonuses.verticalHeader().setStretchLastSection(False)

        self.gridLayout.addWidget(self.best_in_slot_bonuses, 16, 7, 11, 3)

        self.elite_void = QCheckBox(Form)
        self.elite_void.setObjectName(u"elite_void")
        self.elite_void.setChecked(True)

        self.gridLayout.addWidget(self.elite_void, 13, 7, 1, 1)

        self.training_skill = QComboBox(Form)
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.setObjectName(u"training_skill")

        self.gridLayout.addWidget(self.training_skill, 4, 1, 1, 4)

        self.void_knight = QCheckBox(Form)
        self.void_knight.setObjectName(u"void_knight")
        self.void_knight.setChecked(True)

        self.gridLayout.addWidget(self.void_knight, 12, 7, 1, 1)

        self.slayer_helm = QCheckBox(Form)
        self.slayer_helm.setObjectName(u"slayer_helm")
        self.slayer_helm.setChecked(True)

        self.gridLayout.addWidget(self.slayer_helm, 12, 5, 1, 1)

        self.evaluate = QPushButton(Form)
        self.evaluate.setObjectName(u"evaluate")

        self.gridLayout.addWidget(self.evaluate, 14, 0, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.dharok = QLineEdit(Form)
        self.dharok.setObjectName(u"dharok")
        self.dharok.setMaxLength(2)

        self.gridLayout.addWidget(self.dharok, 12, 3, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 14, 1, 1, 9)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.hands_link = QPushButton(self.frame)
        self.hands_link.setObjectName(u"hands_link")

        self.gridLayout_2.addWidget(self.hands_link, 12, 0, 1, 1)

        self.attack_stance = QLineEdit(self.frame)
        self.attack_stance.setObjectName(u"attack_stance")
        self.attack_stance.setEnabled(False)

        self.gridLayout_2.addWidget(self.attack_stance, 15, 2, 1, 1)

        self.xp_rate = QLineEdit(self.frame)
        self.xp_rate.setObjectName(u"xp_rate")
        self.xp_rate.setEnabled(False)
        self.xp_rate.setReadOnly(True)

        self.gridLayout_2.addWidget(self.xp_rate, 16, 2, 1, 1)

        self.weapon_link = QPushButton(self.frame)
        self.weapon_link.setObjectName(u"weapon_link")

        self.gridLayout_2.addWidget(self.weapon_link, 6, 0, 1, 1)

        self.head = QComboBox(self.frame)
        self.head.setObjectName(u"head")

        self.gridLayout_2.addWidget(self.head, 1, 1, 1, 4)

        self.head_link = QPushButton(self.frame)
        self.head_link.setObjectName(u"head_link")

        self.gridLayout_2.addWidget(self.head_link, 1, 0, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 15, 0, 1, 1)

        self.ammo_link = QPushButton(self.frame)
        self.ammo_link.setObjectName(u"ammo_link")

        self.gridLayout_2.addWidget(self.ammo_link, 5, 0, 1, 1)

        self.neck_link = QPushButton(self.frame)
        self.neck_link.setObjectName(u"neck_link")

        self.gridLayout_2.addWidget(self.neck_link, 4, 0, 1, 1)

        self.ring_link = QPushButton(self.frame)
        self.ring_link.setObjectName(u"ring_link")

        self.gridLayout_2.addWidget(self.ring_link, 14, 0, 1, 1)

        self.feet_link = QPushButton(self.frame)
        self.feet_link.setObjectName(u"feet_link")

        self.gridLayout_2.addWidget(self.feet_link, 13, 0, 1, 1)

        self.cape_link = QPushButton(self.frame)
        self.cape_link.setObjectName(u"cape_link")

        self.gridLayout_2.addWidget(self.cape_link, 3, 0, 1, 1)

        self.body_link = QPushButton(self.frame)
        self.body_link.setObjectName(u"body_link")

        self.gridLayout_2.addWidget(self.body_link, 8, 0, 1, 1)

        self.legs_link = QPushButton(self.frame)
        self.legs_link.setObjectName(u"legs_link")

        self.gridLayout_2.addWidget(self.legs_link, 11, 0, 1, 1)

        self.kills_per_hour = QLineEdit(self.frame)
        self.kills_per_hour.setObjectName(u"kills_per_hour")
        self.kills_per_hour.setEnabled(False)

        self.gridLayout_2.addWidget(self.kills_per_hour, 16, 4, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 16, 0, 1, 1)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 15, 3, 1, 1)

        self.kill_time = QLineEdit(self.frame)
        self.kill_time.setObjectName(u"kill_time")
        self.kill_time.setEnabled(False)

        self.gridLayout_2.addWidget(self.kill_time, 15, 4, 1, 1)

        self.shield = QComboBox(self.frame)
        self.shield.setObjectName(u"shield")

        self.gridLayout_2.addWidget(self.shield, 10, 1, 1, 4)

        self.hands = QComboBox(self.frame)
        self.hands.setObjectName(u"hands")

        self.gridLayout_2.addWidget(self.hands, 12, 1, 1, 4)

        self.shield_link = QPushButton(self.frame)
        self.shield_link.setObjectName(u"shield_link")

        self.gridLayout_2.addWidget(self.shield_link, 10, 0, 1, 1)

        self.ring = QComboBox(self.frame)
        self.ring.setObjectName(u"ring")

        self.gridLayout_2.addWidget(self.ring, 14, 1, 1, 4)

        self.legs = QComboBox(self.frame)
        self.legs.setObjectName(u"legs")

        self.gridLayout_2.addWidget(self.legs, 11, 1, 1, 4)

        self.weapon = QComboBox(self.frame)
        self.weapon.setObjectName(u"weapon")

        self.gridLayout_2.addWidget(self.weapon, 6, 1, 1, 4)

        self.ammo = QComboBox(self.frame)
        self.ammo.setObjectName(u"ammo")

        self.gridLayout_2.addWidget(self.ammo, 5, 1, 1, 4)

        self.neck = QComboBox(self.frame)
        self.neck.setObjectName(u"neck")

        self.gridLayout_2.addWidget(self.neck, 4, 1, 1, 4)

        self.cape = QComboBox(self.frame)
        self.cape.setObjectName(u"cape")

        self.gridLayout_2.addWidget(self.cape, 3, 1, 1, 4)

        self.body = QComboBox(self.frame)
        self.body.setObjectName(u"body")

        self.gridLayout_2.addWidget(self.body, 8, 1, 1, 4)

        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 16, 3, 1, 1)

        self.feet = QComboBox(self.frame)
        self.feet.setObjectName(u"feet")

        self.gridLayout_2.addWidget(self.feet, 13, 1, 1, 4)


        self.gridLayout.addWidget(self.frame, 16, 0, 1, 6)

        self.potions = QComboBox(Form)
        self.potions.setObjectName(u"potions")

        self.gridLayout.addWidget(self.potions, 5, 1, 1, 4)

        self.prayer_attributes = QComboBox(Form)
        self.prayer_attributes.addItem("")
        self.prayer_attributes.addItem("")
        self.prayer_attributes.addItem("")
        self.prayer_attributes.setObjectName(u"prayer_attributes")

        self.gridLayout.addWidget(self.prayer_attributes, 10, 5, 1, 3)

        self.boosting_scheme = QComboBox(Form)
        self.boosting_scheme.addItem("")
        self.boosting_scheme.addItem("")
        self.boosting_scheme.setObjectName(u"boosting_scheme")

        self.gridLayout.addWidget(self.boosting_scheme, 5, 8, 1, 2)

        self.berserker_necklace = QCheckBox(Form)
        self.berserker_necklace.setObjectName(u"berserker_necklace")
        self.berserker_necklace.setChecked(True)

        self.gridLayout.addWidget(self.berserker_necklace, 13, 8, 1, 1)

        self.salve_amulet = QCheckBox(Form)
        self.salve_amulet.setObjectName(u"salve_amulet")
        self.salve_amulet.setChecked(True)

        self.gridLayout.addWidget(self.salve_amulet, 13, 5, 1, 1)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 12, 2, 1, 1)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 12, 0, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 10, 0, 1, 1)

        self.opponents = QListWidget(Form)
        self.opponents.setObjectName(u"opponents")
        self.opponents.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)

        self.gridLayout.addWidget(self.opponents, 2, 0, 1, 10)

        self.obsidian = QCheckBox(Form)
        self.obsidian.setObjectName(u"obsidian")
        self.obsidian.setChecked(True)

        self.gridLayout.addWidget(self.obsidian, 12, 8, 1, 1)

        self.redose_level = QLineEdit(Form)
        self.redose_level.setObjectName(u"redose_level")
        self.redose_level.setMaxLength(2)

        self.gridLayout.addWidget(self.redose_level, 7, 8, 1, 1)

        self.prayers = QComboBox(Form)
        self.prayers.setObjectName(u"prayers")

        self.gridLayout.addWidget(self.prayers, 10, 1, 1, 4)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(True)

        self.gridLayout.addWidget(self.label_5, 7, 5, 1, 3)

        self.show_histogram = QCheckBox(Form)
        self.show_histogram.setObjectName(u"show_histogram")

        self.gridLayout.addWidget(self.show_histogram, 15, 2, 1, 1)

        self.label_11 = QLabel(Form)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 4, 5, 1, 1)

        self.cpu_cores = QLineEdit(Form)
        self.cpu_cores.setObjectName(u"cpu_cores")

        self.gridLayout.addWidget(self.cpu_cores, 4, 7, 1, 1)

        QWidget.setTabOrder(self.opponents, self.head_link)
        QWidget.setTabOrder(self.head_link, self.head)
        QWidget.setTabOrder(self.head, self.cape_link)
        QWidget.setTabOrder(self.cape_link, self.cape)
        QWidget.setTabOrder(self.cape, self.neck_link)
        QWidget.setTabOrder(self.neck_link, self.neck)
        QWidget.setTabOrder(self.neck, self.ammo_link)
        QWidget.setTabOrder(self.ammo_link, self.ammo)
        QWidget.setTabOrder(self.ammo, self.weapon_link)
        QWidget.setTabOrder(self.weapon_link, self.weapon)
        QWidget.setTabOrder(self.weapon, self.body_link)
        QWidget.setTabOrder(self.body_link, self.body)
        QWidget.setTabOrder(self.body, self.shield_link)
        QWidget.setTabOrder(self.shield_link, self.shield)
        QWidget.setTabOrder(self.shield, self.hands_link)
        QWidget.setTabOrder(self.hands_link, self.hands)
        QWidget.setTabOrder(self.hands, self.feet_link)
        QWidget.setTabOrder(self.feet_link, self.ring_link)
        QWidget.setTabOrder(self.ring_link, self.ring)
        QWidget.setTabOrder(self.ring, self.xp_rate)
        QWidget.setTabOrder(self.xp_rate, self.best_in_slot_bonuses)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.below_skill.setItemText(0, QCoreApplication.translate("Form", u"attack", None))
        self.below_skill.setItemText(1, QCoreApplication.translate("Form", u"strength", None))
        self.below_skill.setItemText(2, QCoreApplication.translate("Form", u"defence", None))

        self.potion_attributes.setItemText(0, QCoreApplication.translate("Form", u"accuracy", None))
        self.potion_attributes.setItemText(1, QCoreApplication.translate("Form", u"damage", None))
        self.potion_attributes.setItemText(2, QCoreApplication.translate("Form", u"accuracy and damage", None))

        ___qtablewidgetitem = self.best_in_slot_bonuses.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Bonuses", None));
        ___qtablewidgetitem1 = self.best_in_slot_bonuses.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Stab", None));
        ___qtablewidgetitem2 = self.best_in_slot_bonuses.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Slash", None));
        ___qtablewidgetitem3 = self.best_in_slot_bonuses.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Crush", None));
        ___qtablewidgetitem4 = self.best_in_slot_bonuses.verticalHeaderItem(3)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Ranged", None));
        ___qtablewidgetitem5 = self.best_in_slot_bonuses.verticalHeaderItem(4)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Magic", None));
        ___qtablewidgetitem6 = self.best_in_slot_bonuses.verticalHeaderItem(5)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Melee Str", None));
        ___qtablewidgetitem7 = self.best_in_slot_bonuses.verticalHeaderItem(6)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"Ranged Str", None));
        ___qtablewidgetitem8 = self.best_in_slot_bonuses.verticalHeaderItem(7)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"Magic Str", None));
        ___qtablewidgetitem9 = self.best_in_slot_bonuses.verticalHeaderItem(8)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"Speed", None));
        ___qtablewidgetitem10 = self.best_in_slot_bonuses.verticalHeaderItem(9)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"Cost", None));

        __sortingEnabled = self.best_in_slot_bonuses.isSortingEnabled()
        self.best_in_slot_bonuses.setSortingEnabled(False)
        self.best_in_slot_bonuses.setSortingEnabled(__sortingEnabled)

        self.elite_void.setText(QCoreApplication.translate("Form", u"Elite Void", None))
        self.training_skill.setItemText(0, QCoreApplication.translate("Form", u"attack", None))
        self.training_skill.setItemText(1, QCoreApplication.translate("Form", u"strength", None))
        self.training_skill.setItemText(2, QCoreApplication.translate("Form", u"defence", None))
        self.training_skill.setItemText(3, QCoreApplication.translate("Form", u"ranged", None))
        self.training_skill.setItemText(4, QCoreApplication.translate("Form", u"magic", None))

        self.void_knight.setText(QCoreApplication.translate("Form", u"Void", None))
        self.slayer_helm.setText(QCoreApplication.translate("Form", u"Slayer Helm", None))
        self.evaluate.setText(QCoreApplication.translate("Form", u"Evaluate!", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Potions", None))
        self.dharok.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Train", None))
        self.hands_link.setText(QCoreApplication.translate("Form", u"Hands", None))
        self.weapon_link.setText(QCoreApplication.translate("Form", u"Weapon", None))
        self.head_link.setText(QCoreApplication.translate("Form", u"Head", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Attack Stance", None))
        self.ammo_link.setText(QCoreApplication.translate("Form", u"Ammo", None))
        self.neck_link.setText(QCoreApplication.translate("Form", u"Neck", None))
        self.ring_link.setText(QCoreApplication.translate("Form", u"Ring", None))
        self.feet_link.setText(QCoreApplication.translate("Form", u"Feet", None))
        self.cape_link.setText(QCoreApplication.translate("Form", u"Cape", None))
        self.body_link.setText(QCoreApplication.translate("Form", u"Body", None))
        self.legs_link.setText(QCoreApplication.translate("Form", u"Legs", None))
        self.label.setText(QCoreApplication.translate("Form", u"Xp/h", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Kill Time", None))
        self.shield_link.setText(QCoreApplication.translate("Form", u"Shield", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Kills/h", None))
        self.prayer_attributes.setItemText(0, QCoreApplication.translate("Form", u"accuracy", None))
        self.prayer_attributes.setItemText(1, QCoreApplication.translate("Form", u"damage", None))
        self.prayer_attributes.setItemText(2, QCoreApplication.translate("Form", u"accuracy and damage", None))

        self.boosting_scheme.setItemText(0, QCoreApplication.translate("Form", u"Constant", None))
        self.boosting_scheme.setItemText(1, QCoreApplication.translate("Form", u"Dose After", None))

        self.berserker_necklace.setText(QCoreApplication.translate("Form", u"Bers. Neck.", None))
        self.salve_amulet.setText(QCoreApplication.translate("Form", u"Salve Amulet", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"<Dharok HP>", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Other", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Prayer", None))
        self.obsidian.setText(QCoreApplication.translate("Form", u"Obsidian", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"boost below", None))
        self.show_histogram.setText(QCoreApplication.translate("Form", u"Show Histogram", None))
#if QT_CONFIG(tooltip)
        self.label_11.setToolTip(QCoreApplication.translate("Form", u"Number of cores to use during calculations, high values might cause lag.", None))
#endif // QT_CONFIG(tooltip)
        self.label_11.setText(QCoreApplication.translate("Form", u"CPU Cores:", None))
        self.cpu_cores.setText(QCoreApplication.translate("Form", u"0", None))
    # retranslateUi

