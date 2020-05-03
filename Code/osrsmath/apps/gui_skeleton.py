# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_skeleton.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1031, 571)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.xp_rate = QtWidgets.QLineEdit(self.centralwidget)
        self.xp_rate.setReadOnly(True)
        self.xp_rate.setObjectName("xp_rate")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.xp_rate)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.gridLayout_3.addLayout(self.formLayout_2, 12, 2, 1, 1)
        self.input_text_box = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.input_text_box.setObjectName("input_text_box")
        self.gridLayout_3.addWidget(self.input_text_box, 1, 0, 5, 1)
        self.update_database = QtWidgets.QPushButton(self.centralwidget)
        self.update_database.setObjectName("update_database")
        self.gridLayout_3.addWidget(self.update_database, 12, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_3.addWidget(self.comboBox, 6, 4, 1, 1)
        self.evaluate = QtWidgets.QPushButton(self.centralwidget)
        self.evaluate.setObjectName("evaluate")
        self.gridLayout_3.addWidget(self.evaluate, 7, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 0, 1, 15, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 5, 4, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.player_stats = QtWidgets.QRadioButton(self.centralwidget)
        self.player_stats.setChecked(True)
        self.player_stats.setObjectName("player_stats")
        self.EditingOptionGroup = QtWidgets.QButtonGroup(MainWindow)
        self.EditingOptionGroup.setObjectName("EditingOptionGroup")
        self.EditingOptionGroup.addButton(self.player_stats)
        self.gridLayout.addWidget(self.player_stats, 2, 0, 1, 1)
        self.opponents = QtWidgets.QRadioButton(self.centralwidget)
        self.opponents.setObjectName("opponents")
        self.EditingOptionGroup.addButton(self.opponents)
        self.gridLayout.addWidget(self.opponents, 2, 1, 1, 1)
        self.ignore = QtWidgets.QRadioButton(self.centralwidget)
        self.ignore.setObjectName("ignore")
        self.EditingOptionGroup.addButton(self.ignore)
        self.gridLayout.addWidget(self.ignore, 3, 0, 1, 1)
        self.adjustments = QtWidgets.QRadioButton(self.centralwidget)
        self.adjustments.setObjectName("adjustments")
        self.EditingOptionGroup.addButton(self.adjustments)
        self.gridLayout.addWidget(self.adjustments, 3, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.alternate_gear_bonuses = QtWidgets.QTableWidget(self.centralwidget)
        self.alternate_gear_bonuses.setObjectName("alternate_gear_bonuses")
        self.alternate_gear_bonuses.setColumnCount(1)
        self.alternate_gear_bonuses.setRowCount(10)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.alternate_gear_bonuses.setHorizontalHeaderItem(0, item)
        self.alternate_gear_bonuses.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_3.addWidget(self.alternate_gear_bonuses, 1, 5, 8, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.progress_task = QtWidgets.QLabel(self.centralwidget)
        self.progress_task.setObjectName("progress_task")
        self.horizontalLayout.addWidget(self.progress_task)
        self.gridLayout_3.addLayout(self.horizontalLayout, 15, 0, 1, 6)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.best_in_slot_bonuses = QtWidgets.QTableWidget(self.centralwidget)
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
        self.gridLayout_2.addWidget(self.best_in_slot_bonuses, 0, 1, 1, 1)
        self.best_in_slot = QtWidgets.QTableWidget(self.centralwidget)
        self.best_in_slot.setObjectName("best_in_slot")
        self.best_in_slot.setColumnCount(1)
        self.best_in_slot.setRowCount(10)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.best_in_slot.setItem(4, 0, item)
        self.best_in_slot.horizontalHeader().setStretchLastSection(True)
        self.best_in_slot.verticalHeader().setVisible(True)
        self.best_in_slot.verticalHeader().setCascadingSectionResizes(False)
        self.best_in_slot.verticalHeader().setHighlightSections(True)
        self.best_in_slot.verticalHeader().setSortIndicatorShown(False)
        self.gridLayout_2.addWidget(self.best_in_slot, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 2, 10, 1)
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.gridLayout_3.addWidget(self.commandLinkButton, 12, 5, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setChecked(True)
        self.radioButton_4.setObjectName("radioButton_4")
        self.AlternateGearSelectionGroup = QtWidgets.QButtonGroup(MainWindow)
        self.AlternateGearSelectionGroup.setObjectName("AlternateGearSelectionGroup")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_4)
        self.verticalLayout_2.addWidget(self.radioButton_4)
        self.radioButton_5 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_5.setObjectName("radioButton_5")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_5)
        self.verticalLayout_2.addWidget(self.radioButton_5)
        self.radioButton_6 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_6.setObjectName("radioButton_6")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_6)
        self.verticalLayout_2.addWidget(self.radioButton_6)
        self.radioButton_7 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_7.setObjectName("radioButton_7")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_7)
        self.verticalLayout_2.addWidget(self.radioButton_7)
        self.radioButton_8 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_8.setObjectName("radioButton_8")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_8)
        self.verticalLayout_2.addWidget(self.radioButton_8)
        self.radioButton_10 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_10.setObjectName("radioButton_10")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_10)
        self.verticalLayout_2.addWidget(self.radioButton_10)
        self.radioButton_9 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_9.setObjectName("radioButton_9")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_9)
        self.verticalLayout_2.addWidget(self.radioButton_9)
        self.radioButton_11 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_11.setObjectName("radioButton_11")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_11)
        self.verticalLayout_2.addWidget(self.radioButton_11)
        self.radioButton_12 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_12.setObjectName("radioButton_12")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_12)
        self.verticalLayout_2.addWidget(self.radioButton_12)
        self.radioButton_13 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_13.setObjectName("radioButton_13")
        self.AlternateGearSelectionGroup.addButton(self.radioButton_13)
        self.verticalLayout_2.addWidget(self.radioButton_13)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 1, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 4, 1, 2)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setEnabled(True)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_3.addWidget(self.line_2, 0, 3, 11, 1)
        self.training_skill = QtWidgets.QComboBox(self.centralwidget)
        self.training_skill.setObjectName("training_skill")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.training_skill.addItem("")
        self.gridLayout_3.addWidget(self.training_skill, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OSRSmath Optimal Gear Calculator - By Palfore"))
        self.label.setText(_translate("MainWindow", "Experience Rate (k/hr):"))
        self.update_database.setText(_translate("MainWindow", "Update Database"))
        self.evaluate.setText(_translate("MainWindow", "Evaluate!"))
        self.label_3.setText(_translate("MainWindow", "Alternatives:"))
        self.player_stats.setText(_translate("MainWindow", "Player Stats"))
        self.opponents.setText(_translate("MainWindow", "Opponents"))
        self.ignore.setText(_translate("MainWindow", "Ignore"))
        self.adjustments.setText(_translate("MainWindow", "Adjustments"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Stab"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Slash"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Crush"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Ranged"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Magic"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Melee Str"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Ranged Str"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "Magic Str"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "Attack Speed"))
        item = self.alternate_gear_bonuses.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "Cost"))
        item = self.alternate_gear_bonuses.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Difference"))
        self.progress_task.setText(_translate("MainWindow", "Waiting to Evaluate...        "))
        item = self.best_in_slot_bonuses.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Stab"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Slash"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Crush"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Ranged"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Magic"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Melee Str"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Ranged Str"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "Magic Str"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "Attack Speed"))
        item = self.best_in_slot_bonuses.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "Cost"))
        item = self.best_in_slot_bonuses.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Bonuses"))
        __sortingEnabled = self.best_in_slot_bonuses.isSortingEnabled()
        self.best_in_slot_bonuses.setSortingEnabled(False)
        self.best_in_slot_bonuses.setSortingEnabled(__sortingEnabled)
        item = self.best_in_slot.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Head"))
        item = self.best_in_slot.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Cape"))
        item = self.best_in_slot.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Neck"))
        item = self.best_in_slot.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Ammo"))
        item = self.best_in_slot.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Weapon"))
        item = self.best_in_slot.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Body"))
        item = self.best_in_slot.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Shield"))
        item = self.best_in_slot.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "Gloves"))
        item = self.best_in_slot.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "Feet"))
        item = self.best_in_slot.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "Ring"))
        item = self.best_in_slot.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Item"))
        __sortingEnabled = self.best_in_slot.isSortingEnabled()
        self.best_in_slot.setSortingEnabled(False)
        self.best_in_slot.setSortingEnabled(__sortingEnabled)
        self.commandLinkButton.setText(_translate("MainWindow", "Search Item on Wiki"))
        self.radioButton_4.setText(_translate("MainWindow", "Helmet"))
        self.radioButton_5.setText(_translate("MainWindow", "Cape"))
        self.radioButton_6.setText(_translate("MainWindow", "Amulet"))
        self.radioButton_7.setText(_translate("MainWindow", "Ammo"))
        self.radioButton_8.setText(_translate("MainWindow", "Weapon"))
        self.radioButton_10.setText(_translate("MainWindow", "Body"))
        self.radioButton_9.setText(_translate("MainWindow", "Shield"))
        self.radioButton_11.setText(_translate("MainWindow", "Gloves"))
        self.radioButton_12.setText(_translate("MainWindow", "Boots"))
        self.radioButton_13.setText(_translate("MainWindow", "Ring"))
        self.label_4.setText(_translate("MainWindow", "Alternate  Gear Choices"))
        self.training_skill.setItemText(0, _translate("MainWindow", "Train Attack"))
        self.training_skill.setItemText(1, _translate("MainWindow", "Train Strength"))
        self.training_skill.setItemText(2, _translate("MainWindow", "Train Defence"))
        self.training_skill.setItemText(3, _translate("MainWindow", "Train Ranged"))
        self.training_skill.setItemText(4, _translate("MainWindow", "Train Mage"))
        self.label_2.setText(_translate("MainWindow", "Optimal Offensive Gear"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
