import osrsmath.apps.GUI.config as config

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '//mnt/c/Users/Nawar/Documents/GitHub/OSRS-Combat/Code/osrsmath/apps/GUI/optimize/ignore_adjust_skeleton.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IgnoreAdjustPanel(object):
    def setupUi(self, IgnoreAdjustPanel):
        IgnoreAdjustPanel.setObjectName("IgnoreAdjustPanel")
        IgnoreAdjustPanel.resize(267, 254)
        IgnoreAdjustPanel.setMinimumSize(QtCore.QSize(267, 0))
        IgnoreAdjustPanel.setMaximumSize(QtCore.QSize(267, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(IgnoreAdjustPanel)
        self.gridLayout.setObjectName("gridLayout")
        self.ignore = QtWidgets.QRadioButton(IgnoreAdjustPanel)
        self.ignore.setChecked(True)
        self.ignore.setObjectName("ignore")
        self.gridLayout.addWidget(self.ignore, 0, 0, 1, 1)
        self.adjustments = QtWidgets.QRadioButton(IgnoreAdjustPanel)
        self.adjustments.setObjectName("adjustments")
        self.gridLayout.addWidget(self.adjustments, 0, 1, 1, 1)
        self.text = QtWidgets.QPlainTextEdit(IgnoreAdjustPanel)
        self.text.setObjectName("text")
        self.gridLayout.addWidget(self.text, 1, 0, 1, 2)

        self.retranslateUi(IgnoreAdjustPanel)
        QtCore.QMetaObject.connectSlotsByName(IgnoreAdjustPanel)

    def retranslateUi(self, IgnoreAdjustPanel):
        _translate = QtCore.QCoreApplication.translate
        IgnoreAdjustPanel.setWindowTitle(_translate("IgnoreAdjustPanel", "Form"))
        self.ignore.setText(_translate("IgnoreAdjustPanel", "Ignore"))
        self.adjustments.setText(_translate("IgnoreAdjustPanel", "Adjustments"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    IgnoreAdjustPanel = QtWidgets.QWidget()
    ui = Ui_IgnoreAdjustPanel()
    ui.setupUi(IgnoreAdjustPanel)
    IgnoreAdjustPanel.show()
    sys.exit(app.exec_())
