# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ignore_adjust_skeleton.ui'
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


class Ui_IgnoreAdjustPanel(object):
    def setupUi(self, IgnoreAdjustPanel):
        if not IgnoreAdjustPanel.objectName():
            IgnoreAdjustPanel.setObjectName(u"IgnoreAdjustPanel")
        IgnoreAdjustPanel.resize(267, 254)
        IgnoreAdjustPanel.setMinimumSize(QSize(267, 0))
        IgnoreAdjustPanel.setMaximumSize(QSize(267, 16777215))
        self.gridLayout = QGridLayout(IgnoreAdjustPanel)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ignore = QRadioButton(IgnoreAdjustPanel)
        self.ignore.setObjectName(u"ignore")
        self.ignore.setChecked(True)

        self.gridLayout.addWidget(self.ignore, 0, 0, 1, 1)

        self.adjustments = QRadioButton(IgnoreAdjustPanel)
        self.adjustments.setObjectName(u"adjustments")

        self.gridLayout.addWidget(self.adjustments, 0, 1, 1, 1)

        self.text = QPlainTextEdit(IgnoreAdjustPanel)
        self.text.setObjectName(u"text")

        self.gridLayout.addWidget(self.text, 1, 0, 1, 2)


        self.retranslateUi(IgnoreAdjustPanel)

        QMetaObject.connectSlotsByName(IgnoreAdjustPanel)
    # setupUi

    def retranslateUi(self, IgnoreAdjustPanel):
        IgnoreAdjustPanel.setWindowTitle(QCoreApplication.translate("IgnoreAdjustPanel", u"Form", None))
        self.ignore.setText(QCoreApplication.translate("IgnoreAdjustPanel", u"Ignore", None))
        self.adjustments.setText(QCoreApplication.translate("IgnoreAdjustPanel", u"Adjustments", None))
    # retranslateUi

