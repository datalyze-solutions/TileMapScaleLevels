# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TileMapScalePlugin
                                 A QGIS plugin
 Let you add tiled datasets (GDAL WMS) and shows them in the correct scale.
                              -------------------
        begin                : 2014-03-03
        copyright            : (C) 2014 by Matthias Ludwig - Datalyze Solutions
        email                : m.ludwig@datalyze-solutions.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import resources_rc

from tilemapscalelevelswidget import TileMapScaleLevelsDockWidget
from tilemapscalelevels import TileMapScaleLevels

from ui_info import Ui_info

import os.path


class TileMapScalePlugin:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
        # initialize plugin directory
        self.workingDir = os.path.dirname(os.path.abspath(__file__))
        self.datasetDir = os.path.join(self.workingDir, "datasets")
        if not os.path.exists(self.datasetDir):
            self.iface.messageBar().pushMessage("Error", "Can't find %s. You wont't be able to load any datasets." % self.datasetDir, QgsMessageBar.CRITICAL)
            
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.workingDir, 'i18n', 'tilemapscaleplugin_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/tilemapscaleplugin/icon.png"),
            u"TileMapScalePlugin", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.showDock)

        self.dock = TileMapScaleLevelsDockWidget()
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.projection = self.canvas.mapRenderer().destinationCrs()
        self.canvas.enableAntiAliasing(True)

        self.readStatus()
        
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&TileMapScalePlugin", self.action)

        self.scaleCalculator = TileMapScaleLevels(maxZoomlevel=18, minZoomlevel=0, dpi=self.iface.mainWindow().physicalDpiX())
        self.dock.minZoomlevelSpinBox.valueChanged.connect(self.scaleCalculator.setMinZoomlevel)
        self.dock.maxZoomlevelSpinBox.valueChanged.connect(self.scaleCalculator.setMaxZoomlevel)

        self.dock.dpiSpinBox.setValue(self.iface.mainWindow().physicalDpiX())
        self.dock.dpiSpinBox.valueChanged.connect(self.scaleCalculator.setDpi)
        
        self.dock.minZoomlevelSpinBox.valueChanged.connect(self.dock.spinBoxZoomlevels.setMinimum)
        self.dock.maxZoomlevelSpinBox.valueChanged.connect(self.dock.spinBoxZoomlevels.setMaximum)
        self.dock.minZoomlevelSpinBox.valueChanged.connect(self.dock.sliderZoomlevels.setMinimum)
        self.dock.maxZoomlevelSpinBox.valueChanged.connect(self.dock.sliderZoomlevels.setMaximum)
        
        self.dock.spinBoxZoomlevels.setKeyboardTracking(False)
        self.dock.sliderZoomlevels.sliderReleased.connect(self.sliderReleased)
        self.dock.spinBoxZoomlevels.valueChanged.connect(self.valueChanged)

        self.dock.checkBoxIsActive.stateChanged.connect(self.activationStateChanged)
        self.dock.checkBoxUseMercator.stateChanged.connect(self.useMercator)
        self.dock.checkBoxUseOnTheFlyTransformation.stateChanged.connect(self.useOnTheFlyTransformation)

        self.dock.buttonInfo.clicked.connect(self.showInfo)

        self.dock.buttonLoadOSM.clicked.connect(self.loadOSM)
        self.dock.buttonLoadUserDataset.clicked.connect(self.loadSelectedUserDataset)
        self.dock.buttonLoadRefreshUserDatasets.clicked.connect(self.initUserDatasets)      

        self.initUserDatasets()
        self.canvas.scaleChanged.connect(self.scaleChanged)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&TileMapScalePlugin", self.action)
        self.iface.removeToolBarIcon(self.action)

    def showDock(self):
        if self.dock.isVisible():
            self.dock.hide()
        else:
            self.dock.show()

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Tile Map Scale Plugin", self.action)
        self.iface.removeToolBarIcon(self.action)
        self.iface.removeDockWidget(self.dock)

    def showInfo(self):
        self.dialogInfo = dialogInfo(self.workingDir)
        self.dialogInfo.setParent(self.iface.mainWindow(), self.dialogInfo.windowFlags())
        self.dialogInfo.exec_()

    def sliderReleased(self):
        self.dock.spinBoxZoomlevels.setValue(self.dock.sliderZoomlevels.value())

    def valueChanged(self):
        zoomlevel = self.dock.spinBoxZoomlevels.value()
        scale = self.scaleCalculator.getScale(zoomlevel)
        self.scaleChanged(scale)

    def loadOSM(self):
        datasetPath = os.path.join(self.datasetDir, "osm_mapnik.xml")
        if os.path.exists(datasetPath):
            self.iface.addRasterLayer(datasetPath, "OpenStreetMap - Mapnik")
        else:
            self.iface.messageBar().pushMessage("Error", "Unable to load file %s" % datasetPath, QgsMessageBar.CRITICAL)

    def initUserDatasets(self):
        self.dock.comboBoxUserDatasets.clear()
        filenames = os.listdir(self.datasetDir)
        filenames.sort()
        for filename in filenames:
            if not filename.endswith('.xml'): continue
            self.dock.comboBoxUserDatasets.addItem(filename)

    def loadSelectedUserDataset(self):
        selectedDataset = str(self.dock.comboBoxUserDatasets.currentText())
        datasetPath = os.path.join(self.datasetDir, selectedDataset)
        errorMessage = "Unable to load file %s" % datasetPath
        if (selectedDataset == ""):
            self.iface.messageBar().pushMessage("Error", errorMessage, QgsMessageBar.CRITICAL)
        elif os.path.exists(datasetPath):
            self.iface.addRasterLayer(datasetPath, selectedDataset)
        else:
            self.iface.messageBar().pushMessage("Error", errorMessage, QgsMessageBar.CRITICAL)

    def scaleChanged(self, scale):
        if self.dock.checkBoxIsActive.isChecked():
            ## Disconnect to prevent infinite scaling loop
            self.canvas.scaleChanged.disconnect(self.scaleChanged)
            self.dock.spinBoxZoomlevels.valueChanged.disconnect(self.valueChanged)

            zoomlevel = self.scaleCalculator.getZoomlevel(scale)
            if zoomlevel <> None:
                newScale = self.scaleCalculator.getScale(zoomlevel)
                self.canvas.zoomScale(newScale)
                self.dock.sliderZoomlevels.setValue(zoomlevel)
                self.dock.spinBoxZoomlevels.setValue(zoomlevel)

            self.canvas.scaleChanged.connect(self.scaleChanged)
            self.dock.spinBoxZoomlevels.valueChanged.connect(self.valueChanged)

    def activationStateChanged(self):
        if self.dock.checkBoxIsActive.isChecked():
            self.dock.groupBox.show()
        else:
            self.dock.groupBox.hide()
        self.storeStatus()

    def useMercator(self):
        if self.dock.checkBoxUseMercator.isChecked():
            coordinateReferenceSystem = QgsCoordinateReferenceSystem()
            createCrs = coordinateReferenceSystem.createFromString("EPSG:3857")

            if self.projection != coordinateReferenceSystem:
                self.projection = self.canvas.mapRenderer().destinationCrs()

            self.canvas.mapRenderer().setDestinationCrs(coordinateReferenceSystem)
        else:
            self.canvas.mapRenderer().setDestinationCrs(self.projection)

    def useOnTheFlyTransformation(self):
        if self.dock.checkBoxUseOnTheFlyTransformation.isChecked():
            self.canvas.mapRenderer().setProjectionsEnabled(True)
        else:
            self.canvas.mapRenderer().setProjectionsEnabled(False)

    def storeStatus(self):
        s = QSettings()
        s.setValue("tilemapscalelevels/active", self.dock.checkBoxIsActive.isChecked())        

    def readStatus(self):
        s = QSettings()
        isActive = s.value("tilemapscalelevels/active", True, type=bool)
        self.dock.checkBoxIsActive.setChecked(isActive)


class dialogInfo(QDialog, Ui_info):

    def __init__(self, workingDir, infoHtml="README.html"):
        super(dialogInfo, self).__init__()
        self.setupUi(self)

        self.workingDir = workingDir
        self.infoHtml = infoHtml
        self.goHome()
        self.buttonHome.clicked.connect(self.goHome)

    def goHome(self):
        url = os.path.join(self.workingDir, self.infoHtml)
        self.webView.setUrl(QUrl(url))