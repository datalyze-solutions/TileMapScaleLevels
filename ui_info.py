# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_info.ui'
#
# Created: Fri Feb 12 17:34:10 2016
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

class Ui_info(object):
    def setupUi(self, info):
        info.setObjectName(_fromUtf8("info"))
        info.resize(1024, 768)
        self.verticalLayout = QtGui.QVBoxLayout(info)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.buttonHome = QtGui.QToolButton(info)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/go-home.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonHome.setIcon(icon)
        self.buttonHome.setIconSize(QtCore.QSize(22, 22))
        self.buttonHome.setObjectName(_fromUtf8("buttonHome"))
        self.verticalLayout.addWidget(self.buttonHome)
        self.webView = QtWebKit.QWebView(info)
        self.webView.setProperty("url", QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)

        self.retranslateUi(info)
        QtCore.QMetaObject.connectSlotsByName(info)

    def retranslateUi(self, info):
        info.setWindowTitle(_translate("info", "Info", None))
        self.buttonHome.setToolTip(_translate("info", "load selected dataset", None))
        self.buttonHome.setStatusTip(_translate("info", "load selected dataset", None))
        self.buttonHome.setText(_translate("info", "OSM", None))

from PyQt4 import QtWebKit
import resources_rc
