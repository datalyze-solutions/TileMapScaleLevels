# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_hud.ui'
#
# Created: Tue Feb 23 10:18:47 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_hud(object):
    def setupUi(self, hud):
        hud.setObjectName(_fromUtf8("hud"))
        hud.resize(400, 519)
        self.frameButtons = QtGui.QFrame(hud)
        self.frameButtons.setGeometry(QtCore.QRect(10, 10, 51, 261))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameButtons.sizePolicy().hasHeightForWidth())
        self.frameButtons.setSizePolicy(sizePolicy)
        self.frameButtons.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameButtons.setFrameShadow(QtGui.QFrame.Plain)
        self.frameButtons.setObjectName(_fromUtf8("frameButtons"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frameButtons)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setMargin(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.toolButtonLayers = QtGui.QToolButton(self.frameButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/legend.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonLayers.setIcon(icon)
        self.toolButtonLayers.setIconSize(QtCore.QSize(24, 24))
        self.toolButtonLayers.setCheckable(False)
        self.toolButtonLayers.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButtonLayers.setObjectName(_fromUtf8("toolButtonLayers"))
        self.verticalLayout.addWidget(self.toolButtonLayers)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.toolButtonIsActive = QtGui.QToolButton(self.frameButtons)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/toolButtonIsActive.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonIsActive.setIcon(icon1)
        self.toolButtonIsActive.setIconSize(QtCore.QSize(22, 22))
        self.toolButtonIsActive.setCheckable(True)
        self.toolButtonIsActive.setObjectName(_fromUtf8("toolButtonIsActive"))
        self.horizontalLayout_2.addWidget(self.toolButtonIsActive)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.sliderZoomlevels = QtGui.QSlider(self.frameButtons)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sliderZoomlevels.sizePolicy().hasHeightForWidth())
        self.sliderZoomlevels.setSizePolicy(sizePolicy)
        self.sliderZoomlevels.setMaximum(25)
        self.sliderZoomlevels.setTracking(False)
        self.sliderZoomlevels.setOrientation(QtCore.Qt.Vertical)
        self.sliderZoomlevels.setTickPosition(QtGui.QSlider.NoTicks)
        self.sliderZoomlevels.setTickInterval(1)
        self.sliderZoomlevels.setObjectName(_fromUtf8("sliderZoomlevels"))
        self.horizontalLayout_4.addWidget(self.sliderZoomlevels)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.toolButtonTMS = QtGui.QToolButton(hud)
        self.toolButtonTMS.setGeometry(QtCore.QRect(70, 20, 39, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/toolButtonTMS.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonTMS.setIcon(icon2)
        self.toolButtonTMS.setIconSize(QtCore.QSize(24, 24))
        self.toolButtonTMS.setCheckable(True)
        self.toolButtonTMS.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButtonTMS.setObjectName(_fromUtf8("toolButtonTMS"))

        self.retranslateUi(hud)
        QtCore.QMetaObject.connectSlotsByName(hud)

    def retranslateUi(self, hud):
        hud.setWindowTitle(_translate("hud", "Form", None))
        self.frameButtons.setAccessibleName(_translate("hud", "frameMainButtons", None))
        self.toolButtonLayers.setToolTip(_translate("hud", "Add Layers", None))
        self.toolButtonLayers.setStatusTip(_translate("hud", "Add Layers", None))
        self.toolButtonLayers.setText(_translate("hud", "≡", None))
        self.toolButtonIsActive.setToolTip(_translate("hud", "Enable/Disable Scale Levels", None))
        self.toolButtonIsActive.setStatusTip(_translate("hud", "Enable/Disable Scale Levels", None))
        self.toolButtonIsActive.setText(_translate("hud", "o", None))
        self.sliderZoomlevels.setToolTip(_translate("hud", "Zoomlevel", None))
        self.toolButtonTMS.setToolTip(_translate("hud", "Enable/Disable Scale Levels", None))
        self.toolButtonTMS.setStatusTip(_translate("hud", "Enable/Disable Scale Levels", None))
        self.toolButtonTMS.setText(_translate("hud", "≡", None))

import resources_rc
