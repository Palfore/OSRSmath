# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'monsters_skeleton.ui'
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


class Ui_Monsters(object):
    def setupUi(self, Monsters):
        if not Monsters.objectName():
            Monsters.setObjectName(u"Monsters")
        Monsters.resize(578, 451)
        self.gridLayout = QGridLayout(Monsters)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.frame = QFrame(Monsters)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 1, -1, -1)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")

        self.gridLayout_2.addWidget(self.frame_2, 2, 6, 1, 1)

        self.custom_name = QLineEdit(self.frame)
        self.custom_name.setObjectName(u"custom_name")

        self.gridLayout_2.addWidget(self.custom_name, 7, 2, 1, 3)

        self.search = QComboBox(self.frame)
        self.search.setObjectName(u"search")
        self.search.setEditable(True)

        self.gridLayout_2.addWidget(self.search, 0, 2, 1, 3)

        self.image_3 = QFrame(self.frame)
        self.image_3.setObjectName(u"image_3")
        self.image_3.setFrameShape(QFrame.Box)
        self.image_3.setFrameShadow(QFrame.Raised)
        self.image_3.setLineWidth(1)
        self.gridLayout_5 = QGridLayout(self.image_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.defensive_magic = QLineEdit(self.image_3)
        self.defensive_magic.setObjectName(u"defensive_magic")

        self.gridLayout_5.addWidget(self.defensive_magic, 2, 5, 1, 1)

        self.defensive_stab = QLineEdit(self.image_3)
        self.defensive_stab.setObjectName(u"defensive_stab")

        self.gridLayout_5.addWidget(self.defensive_stab, 2, 2, 1, 1)

        self.label_19 = QLabel(self.image_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setPixmap(QPixmap(u":/monster/Ranged_icon.webp"))
        self.label_19.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_19, 1, 6, 1, 1)

        self.defensive_slash = QLineEdit(self.image_3)
        self.defensive_slash.setObjectName(u"defensive_slash")

        self.gridLayout_5.addWidget(self.defensive_slash, 2, 3, 1, 1)

        self.label_16 = QLabel(self.image_3)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setPixmap(QPixmap(u":/monster/White_scimitar.webp"))
        self.label_16.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_16, 1, 3, 1, 1)

        self.label_17 = QLabel(self.image_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setPixmap(QPixmap(u":/monster/White_warhammer.webp"))
        self.label_17.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_17, 1, 4, 1, 1)

        self.label_18 = QLabel(self.image_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setPixmap(QPixmap(u":/monster/Magic_icon.webp"))
        self.label_18.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_18, 1, 5, 1, 1)

        self.frame_6 = QFrame(self.image_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Plain)
        self.frame_6.setLineWidth(3)
        self.gridLayout_9 = QGridLayout(self.frame_6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")

        self.gridLayout_5.addWidget(self.frame_6, 0, 2, 1, 5)

        self.label_25 = QLabel(self.image_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setPixmap(QPixmap(u":/monster/Defence_icon.webp"))
        self.label_25.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_25, 1, 0, 1, 1)

        self.defensive_crush = QLineEdit(self.image_3)
        self.defensive_crush.setObjectName(u"defensive_crush")

        self.gridLayout_5.addWidget(self.defensive_crush, 2, 4, 1, 1)

        self.defensive_ranged = QLineEdit(self.image_3)
        self.defensive_ranged.setObjectName(u"defensive_ranged")

        self.gridLayout_5.addWidget(self.defensive_ranged, 2, 6, 1, 1)

        self.label_15 = QLabel(self.image_3)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setPixmap(QPixmap(u":/monster/White_dagger.webp"))
        self.label_15.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_15, 1, 2, 1, 1)

        self.line = QFrame(self.image_3)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line, 0, 1, 3, 1)

        self.label_26 = QLabel(self.image_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_26, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.image_3, 5, 1, 1, 5)

        self.image = QFrame(self.frame)
        self.image.setObjectName(u"image")
        self.image.setFrameShape(QFrame.Box)
        self.image.setFrameShadow(QFrame.Raised)
        self.image.setLineWidth(1)
        self.gridLayout_3 = QGridLayout(self.image)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.strength = QLineEdit(self.image)
        self.strength.setObjectName(u"strength")

        self.gridLayout_3.addWidget(self.strength, 3, 4, 1, 1)

        self.label_7 = QLabel(self.image)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setPixmap(QPixmap(u":/monster/Magic_icon.webp"))
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_7, 2, 6, 1, 1)

        self.label_3 = QLabel(self.image)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setPixmap(QPixmap(u":/monster/Hitpoints_icon.webp"))
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_3, 2, 2, 1, 1)

        self.label_8 = QLabel(self.image)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setPixmap(QPixmap(u":/monster/Ranged_icon.webp"))
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_8, 2, 7, 1, 1)

        self.line_3 = QFrame(self.image)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_3, 1, 1, 3, 1)

        self.magic = QLineEdit(self.image)
        self.magic.setObjectName(u"magic")

        self.gridLayout_3.addWidget(self.magic, 3, 6, 1, 1)

        self.attack = QLineEdit(self.image)
        self.attack.setObjectName(u"attack")

        self.gridLayout_3.addWidget(self.attack, 3, 3, 1, 1)

        self.label_5 = QLabel(self.image)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setPixmap(QPixmap(u":/monster/Strength_icon.webp"))
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_5, 2, 4, 1, 1)

        self.defence = QLineEdit(self.image)
        self.defence.setObjectName(u"defence")

        self.gridLayout_3.addWidget(self.defence, 3, 5, 1, 1)

        self.frame_3 = QFrame(self.image)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setLineWidth(0)
        self.gridLayout_7 = QGridLayout(self.frame_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_21 = QLabel(self.frame_3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setPixmap(QPixmap(u":/monster/Combat_icon.webp"))
        self.label_21.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_21, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 2, 0, 1, 1)

        self.label_6 = QLabel(self.image)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setPixmap(QPixmap(u":/monster/Defence_icon.webp"))
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_6, 2, 5, 1, 1)

        self.health = QLineEdit(self.image)
        self.health.setObjectName(u"health")

        self.gridLayout_3.addWidget(self.health, 3, 2, 1, 1)

        self.ranged = QLineEdit(self.image)
        self.ranged.setObjectName(u"ranged")

        self.gridLayout_3.addWidget(self.ranged, 3, 7, 1, 1)

        self.label_4 = QLabel(self.image)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setPixmap(QPixmap(u":/monster/Attack_icon.webp"))
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_4, 2, 3, 1, 1)

        self.combat_level = QLineEdit(self.image)
        self.combat_level.setObjectName(u"combat_level")

        self.gridLayout_3.addWidget(self.combat_level, 3, 0, 1, 1)

        self.label_22 = QLabel(self.image)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_22, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.image, 2, 1, 1, 5)

        self.image_2 = QFrame(self.frame)
        self.image_2.setObjectName(u"image_2")
        self.image_2.setFrameShape(QFrame.Box)
        self.image_2.setFrameShadow(QFrame.Raised)
        self.image_2.setLineWidth(1)
        self.gridLayout_4 = QGridLayout(self.image_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.aggressive_attack = QLineEdit(self.image_2)
        self.aggressive_attack.setObjectName(u"aggressive_attack")

        self.gridLayout_4.addWidget(self.aggressive_attack, 2, 2, 1, 1)

        self.aggressive_magic_damage = QLineEdit(self.image_2)
        self.aggressive_magic_damage.setObjectName(u"aggressive_magic_damage")

        self.gridLayout_4.addWidget(self.aggressive_magic_damage, 2, 5, 1, 1)

        self.label_10 = QLabel(self.image_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setPixmap(QPixmap(u":/monster/Strength_icon.webp"))
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_10, 1, 3, 1, 1)

        self.line_2 = QFrame(self.image_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.line_2, 0, 1, 3, 1)

        self.frame_5 = QFrame(self.image_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Plain)
        self.frame_5.setLineWidth(3)
        self.gridLayout_8 = QGridLayout(self.frame_5)
        self.gridLayout_8.setObjectName(u"gridLayout_8")

        self.gridLayout_4.addWidget(self.frame_5, 0, 2, 1, 6)

        self.label_23 = QLabel(self.image_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setPixmap(QPixmap(u":/monster/Attack_icon.webp"))
        self.label_23.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_23, 1, 0, 1, 1)

        self.aggressive_ranged = QLineEdit(self.image_2)
        self.aggressive_ranged.setObjectName(u"aggressive_ranged")

        self.gridLayout_4.addWidget(self.aggressive_ranged, 2, 6, 1, 1)

        self.label_13 = QLabel(self.image_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setPixmap(QPixmap(u":/monster/Ranged_icon.webp"))
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_13, 1, 6, 1, 1)

        self.label_11 = QLabel(self.image_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setPixmap(QPixmap(u":/monster/Magic_icon.webp"))
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_11, 1, 4, 1, 1)

        self.aggressive_strength = QLineEdit(self.image_2)
        self.aggressive_strength.setObjectName(u"aggressive_strength")

        self.gridLayout_4.addWidget(self.aggressive_strength, 2, 3, 1, 1)

        self.label_9 = QLabel(self.image_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setPixmap(QPixmap(u":/monster/Attack_icon.webp"))
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_9, 1, 2, 1, 1)

        self.label_12 = QLabel(self.image_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setPixmap(QPixmap(u":/monster/Magic_Damage_icon.webp"))
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_12, 1, 5, 1, 1)

        self.label_14 = QLabel(self.image_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setPixmap(QPixmap(u":/monster/Ranged_Strength_icon.webp"))
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_14, 1, 7, 1, 1)

        self.aggressive_ranged_strength = QLineEdit(self.image_2)
        self.aggressive_ranged_strength.setObjectName(u"aggressive_ranged_strength")

        self.gridLayout_4.addWidget(self.aggressive_ranged_strength, 2, 7, 1, 1)

        self.aggressive_magic = QLineEdit(self.image_2)
        self.aggressive_magic.setObjectName(u"aggressive_magic")

        self.gridLayout_4.addWidget(self.aggressive_magic, 2, 4, 1, 1)

        self.label_24 = QLabel(self.image_2)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_24, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.image_2, 4, 1, 1, 5)

        self.nmz_only = QCheckBox(self.frame)
        self.nmz_only.setObjectName(u"nmz_only")

        self.gridLayout_2.addWidget(self.nmz_only, 0, 1, 1, 1)

        self.label_27 = QLabel(self.frame)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_2.addWidget(self.label_27, 7, 1, 1, 1)

        self.add = QPushButton(self.frame)
        self.add.setObjectName(u"add")

        self.gridLayout_2.addWidget(self.add, 7, 5, 1, 1)

        self.wiki_link = QPushButton(self.frame)
        self.wiki_link.setObjectName(u"wiki_link")

        self.gridLayout_2.addWidget(self.wiki_link, 0, 5, 1, 1)

        self.label_20 = QLabel(self.frame)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_20, 6, 1, 1, 1)

        self.xp_per_hit = QLineEdit(self.frame)
        self.xp_per_hit.setObjectName(u"xp_per_hit")
        self.xp_per_hit.setEnabled(False)

        self.gridLayout_2.addWidget(self.xp_per_hit, 6, 2, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        QWidget.setTabOrder(self.nmz_only, self.search)
        QWidget.setTabOrder(self.search, self.wiki_link)
        QWidget.setTabOrder(self.wiki_link, self.combat_level)
        QWidget.setTabOrder(self.combat_level, self.health)
        QWidget.setTabOrder(self.health, self.attack)
        QWidget.setTabOrder(self.attack, self.strength)
        QWidget.setTabOrder(self.strength, self.defence)
        QWidget.setTabOrder(self.defence, self.magic)
        QWidget.setTabOrder(self.magic, self.ranged)
        QWidget.setTabOrder(self.ranged, self.aggressive_attack)
        QWidget.setTabOrder(self.aggressive_attack, self.aggressive_strength)
        QWidget.setTabOrder(self.aggressive_strength, self.aggressive_magic)
        QWidget.setTabOrder(self.aggressive_magic, self.aggressive_magic_damage)
        QWidget.setTabOrder(self.aggressive_magic_damage, self.aggressive_ranged)
        QWidget.setTabOrder(self.aggressive_ranged, self.aggressive_ranged_strength)
        QWidget.setTabOrder(self.aggressive_ranged_strength, self.defensive_stab)
        QWidget.setTabOrder(self.defensive_stab, self.defensive_slash)
        QWidget.setTabOrder(self.defensive_slash, self.defensive_crush)
        QWidget.setTabOrder(self.defensive_crush, self.defensive_magic)
        QWidget.setTabOrder(self.defensive_magic, self.defensive_ranged)
        QWidget.setTabOrder(self.defensive_ranged, self.xp_per_hit)
        QWidget.setTabOrder(self.xp_per_hit, self.custom_name)
        QWidget.setTabOrder(self.custom_name, self.add)

        self.retranslateUi(Monsters)

        QMetaObject.connectSlotsByName(Monsters)
    # setupUi

    def retranslateUi(self, Monsters):
        Monsters.setWindowTitle(QCoreApplication.translate("Monsters", u"Form", None))
        self.label_19.setText("")
        self.label_16.setText("")
        self.label_17.setText("")
        self.label_18.setText("")
        self.label_25.setText("")
        self.label_15.setText("")
        self.label_26.setText(QCoreApplication.translate("Monsters", u" Defensive Stats ", None))
        self.label_7.setText("")
        self.label_3.setText("")
        self.label_8.setText("")
        self.label_5.setText("")
        self.label_21.setText("")
        self.label_6.setText("")
        self.label_4.setText("")
        self.label_22.setText(QCoreApplication.translate("Monsters", u"   Combat Stats  ", None))
        self.label_10.setText("")
        self.label_23.setText("")
        self.label_13.setText("")
        self.label_11.setText("")
        self.label_9.setText("")
        self.label_12.setText("")
        self.label_14.setText("")
        self.label_24.setText(QCoreApplication.translate("Monsters", u"Aggressive Stats", None))
        self.nmz_only.setText(QCoreApplication.translate("Monsters", u"NMZ only", None))
        self.label_27.setText(QCoreApplication.translate("Monsters", u"Custom Name", None))
        self.add.setText(QCoreApplication.translate("Monsters", u"Add", None))
        self.wiki_link.setText(QCoreApplication.translate("Monsters", u"See on Wiki", None))
        self.label_20.setText(QCoreApplication.translate("Monsters", u"xp/damage", None))
#if QT_CONFIG(tooltip)
        self.xp_per_hit.setToolTip(QCoreApplication.translate("Monsters", u"Not supported, you may instead multiply your xp rate by the desired amount.", None))
#endif // QT_CONFIG(tooltip)
        self.xp_per_hit.setText(QCoreApplication.translate("Monsters", u"4", None))
    # retranslateUi

