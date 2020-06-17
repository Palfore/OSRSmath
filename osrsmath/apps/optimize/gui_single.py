# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_single.ui'
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

from osrsmath.apps.monsters.panel import MonsterPanel
from osrsmath.apps.optimize.panels.player import PlayerPanel
from osrsmath.apps.optimize.panels.ignore_adjust import IgnoreAdjustPanel
from osrsmath.apps.optimize.panels.optimize import OptimizePanel


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1002, 583)
        icon = QIcon()
        icon.addFile(u"../GUI/images/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionOverview = QAction(MainWindow)
        self.actionOverview.setObjectName(u"actionOverview")
        self.actionChange_Style = QAction(MainWindow)
        self.actionChange_Style.setObjectName(u"actionChange_Style")
        self.actionIncrease_Size = QAction(MainWindow)
        self.actionIncrease_Size.setObjectName(u"actionIncrease_Size")
        self.actionDecrease_Size = QAction(MainWindow)
        self.actionDecrease_Size.setObjectName(u"actionDecrease_Size")
        self.actionPlayer_Panel = QAction(MainWindow)
        self.actionPlayer_Panel.setObjectName(u"actionPlayer_Panel")
        self.actionMonster_Panel = QAction(MainWindow)
        self.actionMonster_Panel.setObjectName(u"actionMonster_Panel")
        self.actionOptimize_Panel = QAction(MainWindow)
        self.actionOptimize_Panel.setObjectName(u"actionOptimize_Panel")
        self.actionShortcuts = QAction(MainWindow)
        self.actionShortcuts.setObjectName(u"actionShortcuts")
        self.actionUpdate_Now = QAction(MainWindow)
        self.actionUpdate_Now.setObjectName(u"actionUpdate_Now")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(388, 0))
        self.frame_2.setMaximumSize(QSize(388, 16777215))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setLineWidth(3)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.monster_panel = MonsterPanel(self.frame_2)
        self.monster_panel.setObjectName(u"monster_panel")

        self.horizontalLayout_2.addWidget(self.monster_panel)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setEnabled(True)
        self.frame.setMinimumSize(QSize(388, 0))
        self.frame.setMaximumSize(QSize(388, 16777215))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.player_panel = PlayerPanel(self.frame)
        self.player_panel.setObjectName(u"player_panel")

        self.horizontalLayout.addWidget(self.player_panel)

        self.ignore_adjust_panel = IgnoreAdjustPanel(self.frame)
        self.ignore_adjust_panel.setObjectName(u"ignore_adjust_panel")

        self.horizontalLayout.addWidget(self.ignore_adjust_panel)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1, Qt.AlignHCenter)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(588, 0))
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setLineWidth(3)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.optimize_panel = OptimizePanel(self.frame_3)
        self.optimize_panel.setObjectName(u"optimize_panel")

        self.gridLayout_4.addWidget(self.optimize_panel, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 0, 1, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1002, 21))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuFont = QMenu(self.menubar)
        self.menuFont.setObjectName(u"menuFont")
        self.menuUpdate = QMenu(self.menubar)
        self.menuUpdate.setObjectName(u"menuUpdate")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuFont.menuAction())
        self.menubar.addAction(self.menuUpdate.menuAction())
        self.menuHelp.addAction(self.actionOverview)
        self.menuHelp.addAction(self.actionPlayer_Panel)
        self.menuHelp.addAction(self.actionMonster_Panel)
        self.menuHelp.addAction(self.actionOptimize_Panel)
        self.menuHelp.addAction(self.actionShortcuts)
        self.menuFont.addAction(self.actionIncrease_Size)
        self.menuFont.addAction(self.actionDecrease_Size)
        self.menuUpdate.addAction(self.actionUpdate_Now)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OSRS Combat Optimizer", None))
        self.actionOverview.setText(QCoreApplication.translate("MainWindow", u"Overview", None))
        self.actionChange_Style.setText(QCoreApplication.translate("MainWindow", u"Change Style", None))
        self.actionIncrease_Size.setText(QCoreApplication.translate("MainWindow", u"Increase Size", None))
        self.actionDecrease_Size.setText(QCoreApplication.translate("MainWindow", u"Decrease Size", None))
        self.actionPlayer_Panel.setText(QCoreApplication.translate("MainWindow", u"Player Panel", None))
        self.actionMonster_Panel.setText(QCoreApplication.translate("MainWindow", u"Monster Panel", None))
        self.actionOptimize_Panel.setText(QCoreApplication.translate("MainWindow", u"Optimize Panel", None))
        self.actionShortcuts.setText(QCoreApplication.translate("MainWindow", u"Shortcuts", None))
        self.actionUpdate_Now.setText(QCoreApplication.translate("MainWindow", u"Update Now", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"Style", None))
        self.menuFont.setTitle(QCoreApplication.translate("MainWindow", u"Font", None))
        self.menuUpdate.setTitle(QCoreApplication.translate("MainWindow", u"Update", None))
    # retranslateUi

