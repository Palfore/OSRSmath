import osrsmath.apps.GUI.config as config

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '//mnt/c/Users/Nawar/Documents/GitHub/OSRS-Combat/Code/osrsmath/apps/GUI/optimize/optimize_skeleton.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(714, 738)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.hands_link = QtWidgets.QPushButton(self.frame)
        self.hands_link.setObjectName("hands_link")
        self.gridLayout_2.addWidget(self.hands_link, 12, 1, 1, 1)
        self.neck = QtWidgets.QComboBox(self.frame)
        self.neck.setObjectName("neck")
        self.gridLayout_2.addWidget(self.neck, 4, 2, 1, 2)
        self.ring = QtWidgets.QComboBox(self.frame)
        self.ring.setObjectName("ring")
        self.gridLayout_2.addWidget(self.ring, 14, 2, 1, 2)
        self.weapon = QtWidgets.QComboBox(self.frame)
        self.weapon.setObjectName("weapon")
        self.gridLayout_2.addWidget(self.weapon, 6, 2, 1, 2)
        self.ammo_link = QtWidgets.QPushButton(self.frame)
        self.ammo_link.setObjectName("ammo_link")
        self.gridLayout_2.addWidget(self.ammo_link, 5, 1, 1, 1)
        self.shield = QtWidgets.QComboBox(self.frame)
        self.shield.setObjectName("shield")
        self.gridLayout_2.addWidget(self.shield, 10, 2, 1, 2)
        self.ammo = QtWidgets.QComboBox(self.frame)
        self.ammo.setObjectName("ammo")
        self.gridLayout_2.addWidget(self.ammo, 5, 2, 1, 2)
        self.hands = QtWidgets.QComboBox(self.frame)
        self.hands.setObjectName("hands")
        self.gridLayout_2.addWidget(self.hands, 12, 2, 1, 2)
        self.cape = QtWidgets.QComboBox(self.frame)
        self.cape.setObjectName("cape")
        self.gridLayout_2.addWidget(self.cape, 3, 2, 1, 2)
        self.head = QtWidgets.QComboBox(self.frame)
        self.head.setObjectName("head")
        self.gridLayout_2.addWidget(self.head, 1, 2, 1, 2)
        self.legs = QtWidgets.QComboBox(self.frame)
        self.legs.setObjectName("legs")
        self.gridLayout_2.addWidget(self.legs, 11, 2, 1, 2)
        self.cape_link = QtWidgets.QPushButton(self.frame)
        self.cape_link.setObjectName("cape_link")
        self.gridLayout_2.addWidget(self.cape_link, 3, 1, 1, 1)
        self.feet_link = QtWidgets.QPushButton(self.frame)
        self.feet_link.setObjectName("feet_link")
        self.gridLayout_2.addWidget(self.feet_link, 13, 1, 1, 1)
        self.body_link = QtWidgets.QPushButton(self.frame)
        self.body_link.setObjectName("body_link")
        self.gridLayout_2.addWidget(self.body_link, 8, 1, 1, 1)
        self.ring_link = QtWidgets.QPushButton(self.frame)
        self.ring_link.setObjectName("ring_link")
        self.gridLayout_2.addWidget(self.ring_link, 14, 1, 1, 1)
        self.legs_link = QtWidgets.QPushButton(self.frame)
        self.legs_link.setObjectName("legs_link")
        self.gridLayout_2.addWidget(self.legs_link, 11, 1, 1, 1)
        self.neck_link = QtWidgets.QPushButton(self.frame)
        self.neck_link.setObjectName("neck_link")
        self.gridLayout_2.addWidget(self.neck_link, 4, 1, 1, 1)
        self.body = QtWidgets.QComboBox(self.frame)
        self.body.setObjectName("body")
        self.gridLayout_2.addWidget(self.body, 8, 2, 1, 2)
        self.feet = QtWidgets.QComboBox(self.frame)
        self.feet.setObjectName("feet")
        self.gridLayout_2.addWidget(self.feet, 13, 2, 1, 2)
        self.shield_link = QtWidgets.QPushButton(self.frame)
        self.shield_link.setObjectName("shield_link")
        self.gridLayout_2.addWidget(self.shield_link, 10, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 16, 1, 1, 1)
        self.head_link = QtWidgets.QPushButton(self.frame)
        self.head_link.setObjectName("head_link")
        self.gridLayout_2.addWidget(self.head_link, 1, 1, 1, 1)
        self.weapon_link = QtWidgets.QPushButton(self.frame)
        self.weapon_link.setObjectName("weapon_link")
        self.gridLayout_2.addWidget(self.weapon_link, 6, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 15, 1, 1, 1)
        self.xp_rate = QtWidgets.QLineEdit(self.frame)
        self.xp_rate.setEnabled(False)
        self.xp_rate.setReadOnly(True)
        self.xp_rate.setObjectName("xp_rate")
        self.gridLayout_2.addWidget(self.xp_rate, 16, 3, 1, 1)
        self.attack_stance = QtWidgets.QLineEdit(self.frame)
        self.attack_stance.setEnabled(False)
        self.attack_stance.setObjectName("attack_stance")
        self.gridLayout_2.addWidget(self.attack_stance, 15, 3, 1, 1)
        self.gridLayout.addWidget(self.frame, 13, 0, 1, 6)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 10, 0, 1, 1)
        self.below_skill = QtWidgets.QComboBox(Form)
        self.below_skill.setObjectName("below_skill")
        self.below_skill.addItem("")
        self.below_skill.addItem("")
        self.below_skill.addItem("")
        self.gridLayout.addWidget(self.below_skill, 7, 2, 1, 4)
        self.training_skill = QtWidgets.QComboBox(Form)
        self.training_skill.setObjectName("training_skill")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.gridLayout.addWidget(self.training_skill, 4, 2, 1, 5)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setEnabled(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 7, 1, 1)
        self.opponents = QtWidgets.QListWidget(Form)
        self.opponents.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.opponents.setObjectName("opponents")
        self.gridLayout.addWidget(self.opponents, 2, 0, 1, 10)
        self.evaluate = QtWidgets.QPushButton(Form)
        self.evaluate.setObjectName("evaluate")
        self.gridLayout.addWidget(self.evaluate, 12, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.potion_attributes = QtWidgets.QComboBox(Form)
        self.potion_attributes.setObjectName("potion_attributes")
        self.potion_attributes.addItem("")
        self.potion_attributes.addItem("")
        self.potion_attributes.addItem("")
        self.gridLayout.addWidget(self.potion_attributes, 5, 7, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 12, 2, 1, 8)
        self.best_in_slot_bonuses = QtWidgets.QTableWidget(Form)
        self.best_in_slot_bonuses.setShowGrid(True)
        self.best_in_slot_bonuses.setObjectName("best_in_slot_bonuses")
        self.best_in_slot_bonuses.setColumnCount(1)
        self.best_in_slot_bonuses.setRowCount(10)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot_bonuses.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.best_in_slot_bonuses.setItem(9, 0, item)
        self.best_in_slot_bonuses.horizontalHeader().setStretchLastSection(True)
        self.best_in_slot_bonuses.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.best_in_slot_bonuses, 13, 6, 11, 4)
        self.potions = QtWidgets.QComboBox(Form)
        self.potions.setObjectName("potions")
        self.gridLayout.addWidget(self.potions, 5, 2, 1, 5)
        self.boosting_scheme = QtWidgets.QComboBox(Form)
        self.boosting_scheme.setObjectName("boosting_scheme")
        self.boosting_scheme.addItem("")
        self.boosting_scheme.addItem("")
        self.gridLayout.addWidget(self.boosting_scheme, 5, 8, 1, 1)
        self.redose_level = QtWidgets.QLineEdit(Form)
        self.redose_level.setMaxLength(2)
        self.redose_level.setObjectName("redose_level")
        self.gridLayout.addWidget(self.redose_level, 7, 8, 1, 1)
        self.prayers = QtWidgets.QComboBox(Form)
        self.prayers.setObjectName("prayers")
        self.gridLayout.addWidget(self.prayers, 10, 2, 1, 5)
        self.prayer_attributes = QtWidgets.QComboBox(Form)
        self.prayer_attributes.setObjectName("prayer_attributes")
        self.prayer_attributes.addItem("")
        self.prayer_attributes.addItem("")
        self.prayer_attributes.addItem("")
        self.gridLayout.addWidget(self.prayer_attributes, 10, 7, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.opponents, self.head_link)
        Form.setTabOrder(self.head_link, self.head)
        Form.setTabOrder(self.head, self.cape_link)
        Form.setTabOrder(self.cape_link, self.cape)
        Form.setTabOrder(self.cape, self.neck_link)
        Form.setTabOrder(self.neck_link, self.neck)
        Form.setTabOrder(self.neck, self.ammo_link)
        Form.setTabOrder(self.ammo_link, self.ammo)
        Form.setTabOrder(self.ammo, self.weapon_link)
        Form.setTabOrder(self.weapon_link, self.weapon)
        Form.setTabOrder(self.weapon, self.body_link)
        Form.setTabOrder(self.body_link, self.body)
        Form.setTabOrder(self.body, self.shield_link)
        Form.setTabOrder(self.shield_link, self.shield)
        Form.setTabOrder(self.shield, self.hands_link)
        Form.setTabOrder(self.hands_link, self.hands)
        Form.setTabOrder(self.hands, self.feet_link)
        Form.setTabOrder(self.feet_link, self.feet)
        Form.setTabOrder(self.feet, self.ring_link)
        Form.setTabOrder(self.ring_link, self.ring)
        Form.setTabOrder(self.ring, self.xp_rate)
        Form.setTabOrder(self.xp_rate, self.best_in_slot_bonuses)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.hands_link.setText(_translate("Form", "Hands"))
        self.ammo_link.setText(_translate("Form", "Ammo"))
        self.cape_link.setText(_translate("Form", "Cape"))
        self.feet_link.setText(_translate("Form", "Feet"))
        self.body_link.setText(_translate("Form", "Body"))
        self.ring_link.setText(_translate("Form", "Ring"))
        self.legs_link.setText(_translate("Form", "Legs"))
        self.neck_link.setText(_translate("Form", "Neck"))
        self.shield_link.setText(_translate("Form", "Shield"))
        self.label.setText(_translate("Form", "Xp/h"))
        self.head_link.setText(_translate("Form", "Head"))
        self.weapon_link.setText(_translate("Form", "Weapon"))
        self.label_2.setText(_translate("Form", "Attack Stance"))
        self.label_3.setText(_translate("Form", "Potions"))
        self.label_4.setText(_translate("Form", "Prayer"))
        self.below_skill.setItemText(0, _translate("Form", "attack"))
        self.below_skill.setItemText(1, _translate("Form", "strength"))
        self.below_skill.setItemText(2, _translate("Form", "defence"))
        self.training_skill.setItemText(0, _translate("Form", "attack"))
        self.training_skill.setItemText(1, _translate("Form", "strength"))
        self.training_skill.setItemText(2, _translate("Form", "defence"))
        self.training_skill.setItemText(3, _translate("Form", "ranged"))
        self.training_skill.setItemText(4, _translate("Form", "magic"))
        self.label_5.setText(_translate("Form", "boost below"))
        self.evaluate.setText(_translate("Form", "Evaluate!"))
        self.label_6.setText(_translate("Form", "Train"))
        self.potion_attributes.setItemText(0, _translate("Form", "accuracy"))
        self.potion_attributes.setItemText(1, _translate("Form", "damage"))
        self.potion_attributes.setItemText(2, _translate("Form", "accuracy and damage"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(0)
        item.setText(_translate("Form", "Stab"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(1)
        item.setText(_translate("Form", "Slash"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(2)
        item.setText(_translate("Form", "Crush"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(3)
        item.setText(_translate("Form", "Ranged"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(4)
        item.setText(_translate("Form", "Magic"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(5)
        item.setText(_translate("Form", "Melee Str"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(6)
        item.setText(_translate("Form", "Ranged Str"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(7)
        item.setText(_translate("Form", "Magic Str"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(8)
        item.setText(_translate("Form", "Attack Speed"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(9)
        item.setText(_translate("Form", "Cost"))
        item = self.best_in_slot_bonuses.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Bonuses"))
        __sortingEnabled = self.best_in_slot_bonuses.isSortingEnabled()
        self.best_in_slot_bonuses.setSortingEnabled(False)
        self.best_in_slot_bonuses.setSortingEnabled(__sortingEnabled)
        self.boosting_scheme.setItemText(0, _translate("Form", "Constant"))
        self.boosting_scheme.setItemText(1, _translate("Form", "Dose After"))
        self.prayer_attributes.setItemText(0, _translate("Form", "accuracy"))
        self.prayer_attributes.setItemText(1, _translate("Form", "damage"))
        self.prayer_attributes.setItemText(2, _translate("Form", "damage and accuracy"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
