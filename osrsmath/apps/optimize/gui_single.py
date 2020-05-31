# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '//mnt/c/Users/Nawar/Documents/GitHub/OSRSmath/osrsmath/apps/optimize/gui_single.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1002, 583)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//mnt/c/Users/Nawar/Documents/GitHub/OSRSmath/osrsmath/apps/optimize/../GUI/images/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(388, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(388, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(3)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.monster_panel = MonsterPanel(self.frame_2)
        self.monster_panel.setObjectName("monster_panel")
        self.horizontalLayout_2.addWidget(self.monster_panel)
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        self.frame.setMinimumSize(QtCore.QSize(388, 0))
        self.frame.setMaximumSize(QtCore.QSize(388, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.player_panel = PlayerPanel(self.frame)
        self.player_panel.setObjectName("player_panel")
        self.horizontalLayout.addWidget(self.player_panel)
        self.ignore_adjust_panel = IgnoreAdjustPanel(self.frame)
        self.ignore_adjust_panel.setObjectName("ignore_adjust_panel")
        self.horizontalLayout.addWidget(self.ignore_adjust_panel)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMinimumSize(QtCore.QSize(588, 0))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(3)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.optimize_panel = OptimizePanel(self.frame_3)
        self.optimize_panel.setObjectName("optimize_panel")
        self.gridLayout_4.addWidget(self.optimize_panel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 0, 1, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1002, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuFont = QtWidgets.QMenu(self.menubar)
        self.menuFont.setObjectName("menuFont")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOverview = QtWidgets.QAction(MainWindow)
        self.actionOverview.setObjectName("actionOverview")
        self.actionChange_Style = QtWidgets.QAction(MainWindow)
        self.actionChange_Style.setObjectName("actionChange_Style")
        self.actionIncrease_Size = QtWidgets.QAction(MainWindow)
        self.actionIncrease_Size.setObjectName("actionIncrease_Size")
        self.actionDecrease_Size = QtWidgets.QAction(MainWindow)
        self.actionDecrease_Size.setObjectName("actionDecrease_Size")
        self.menuHelp.addAction(self.actionOverview)
        self.menuFont.addAction(self.actionIncrease_Size)
        self.menuFont.addAction(self.actionDecrease_Size)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuFont.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OSRS Combat Optimizer"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuView.setTitle(_translate("MainWindow", "Style"))
        self.menuFont.setTitle(_translate("MainWindow", "Font"))
        self.actionOverview.setText(_translate("MainWindow", "Overview"))
        self.actionChange_Style.setText(_translate("MainWindow", "Change Style"))
        self.actionIncrease_Size.setText(_translate("MainWindow", "Increase Size"))
        self.actionDecrease_Size.setText(_translate("MainWindow", "Decrease Size"))
from osrsmath.apps.monsters.panel import MonsterPanel
from osrsmath.apps.optimize.panels.ignore_adjust import IgnoreAdjustPanel
from osrsmath.apps.optimize.panels.optimize import OptimizePanel
from osrsmath.apps.optimize.panels.player import PlayerPanel


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
