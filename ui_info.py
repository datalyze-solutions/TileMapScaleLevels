# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_info.ui'
#
# Created: Mon Mar  3 16:55:16 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_info(object):
    def setupUi(self, info):
        info.setObjectName(_fromUtf8("info"))
        info.resize(818, 724)
        self.verticalLayout = QtGui.QVBoxLayout(info)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.buttonHome = QtGui.QToolButton(info)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/go-home.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonHome.setIcon(icon)
        self.buttonHome.setIconSize(QtCore.QSize(22, 22))
        self.buttonHome.setObjectName(_fromUtf8("buttonHome"))
        self.verticalLayout.addWidget(self.buttonHome)
        self.webView = QtWebKit.QWebView(info)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)

        self.retranslateUi(info)
        QtCore.QMetaObject.connectSlotsByName(info)

    def retranslateUi(self, info):
        info.setWindowTitle(QtGui.QApplication.translate("info", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonHome.setToolTip(QtGui.QApplication.translate("info", "load selected dataset", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonHome.setStatusTip(QtGui.QApplication.translate("info", "load selected dataset", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonHome.setText(QtGui.QApplication.translate("info", "OSM", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
import resources_rc
