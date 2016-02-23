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
from PyQt4.QtSvg import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
from qgis.core import *
from qgis.gui import *

from tms.canvas_adapter import TileMapServiceCanvasAdapter
from utils.state_store import StateStore
import resources_rc
from utils.colors import FLAT_RED, FLAT_GREEN, FLAT_BLUE

from tilemapscalelevelswidget import TileMapScaleLevelsDockWidget

from ui_info import Ui_info
from ui_hud import Ui_hud

import os.path

class TileMapScalePlugin(QObject):

    def __init__(self, iface):
        super(TileMapScalePlugin, self).__init__(None)
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.canvasAdapter = TileMapServiceCanvasAdapter(self.canvas, 0, 18)
        self._actions = []

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

        self._pluginName = u"Tile Map Scale Levels"

    def initGui(self):
        # init variables as StateStore to bind gui elements later
        self.states = StateStore()
        self.states.add("isActive", self.readStatus())
        self.states.add("zoomlevel", 0)
        self.states.add("minZoomlevel", 0)
        self.states.add("maxZoomlevel", 18)
        self.states.add("showHUD", True)
        self.states.add("showDock", True)
        self.states.add("dpi", self.canvasAdapter.dpi())

        # basic canvas variables
        self.projection = self.canvas.mapSettings().destinationCrs()
        self.canvas.enableAntiAliasing(True)

        # init gui elements
        self.hud = HUD(self.canvas)
        self.dock = TileMapScaleLevelsDockWidget()
        self.dock.tabWidget.setCurrentIndex(0)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        # TODO: activate button and add functionality to add new datasets from interface
        self.dock.buttonLoadUserDataset.hide()

        # connect slots and register gui and StateStore
        # dock
        self.states.showDock.register(self.dock, "setVisible", bool)
        self.states.showDock.register(self.dock.actionTMS, "setChecked", bool)
        self.dock.actionTMS.triggered.connect(self.states.showDock.setValue)
        self.dock.visibilityChanged.connect(self.states.showDock.setValue)
        self.dock.visibilityChanged.connect(self._updateCheckedComponents)
        self.hud.toolButtonTMS.toggled.connect(self.switchIsActiveIcon)
        self.dock.actionTMS.toggled.connect(self.switchIsActiveIcon)

        # HUD
        self.states.showHUD.register(self.hud.frameButtons, "setVisible", bool)
        self.states.showHUD.register(self.dock.checkBoxHUD, "setChecked", bool)
        self.states.showHUD.register(self.dock.actionHUD, "setChecked", bool)
        self.dock.actionHUD.triggered.connect(self.states.showHUD.setValue)
        self.dock.buttonInfo.clicked.connect(self.showInfo)
        self.dock.checkBoxHUD.stateChanged.connect(self.states.showHUD.setValue)
        self.dock.actionHUD.toggled.connect(self.switchIsActiveIcon)
        self.dock.checkBoxHUD.stateChanged.connect(self._updateCheckedComponents)

        # zoomlevel
        self.states.zoomlevel.register(self.hud.sliderZoomlevels, "setValue", int)
        self.states.zoomlevel.register(self.dock.sliderZoomlevels, "setValue", int)
        self.states.zoomlevel.register(self.dock.spinBoxZoomlevels, "setValue", int)
        self.canvasAdapter.zoomlevelChanged.connect(self.states.zoomlevel.setValue)
        self.dock.spinBoxZoomlevels.valueChanged.connect(self.canvasAdapter.zoomZoomlevel)
        self.dock.sliderZoomlevels.valueChanged.connect(self.canvasAdapter.zoomZoomlevel)
        self.hud.sliderZoomlevels.valueChanged.connect(self.canvasAdapter.zoomZoomlevel)

        # minZoomlevel
        self.states.minZoomlevel.register(self.dock.minZoomlevelSpinBox, "setValue", int)
        self.states.minZoomlevel.register(self.dock.sliderZoomlevels, "setMinimum", int)
        self.states.minZoomlevel.register(self.dock.spinBoxZoomlevels, "setMinimum", int)
        self.states.minZoomlevel.register(self.hud.sliderZoomlevels, "setMinimum", int)
        self.dock.minZoomlevelSpinBox.valueChanged.connect(self.canvasAdapter.setMinZoomlevel)
        self.canvasAdapter.minZoomlevelChanged.connect(self.states.minZoomlevel.setValue)

        # maxZoomlevel
        self.states.maxZoomlevel.register(self.dock.maxZoomlevelSpinBox, "setValue", int)
        self.states.maxZoomlevel.register(self.dock.sliderZoomlevels, "setMaximum", int)
        self.states.maxZoomlevel.register(self.dock.spinBoxZoomlevels, "setMaximum", int)
        self.states.maxZoomlevel.register(self.hud.sliderZoomlevels, "setMaximum", int)
        self.dock.maxZoomlevelSpinBox.valueChanged.connect(self.canvasAdapter.setMaxZoomlevel)
        self.canvasAdapter.maxZoomlevelChanged.connect(self.states.maxZoomlevel.setValue)

        # isActive
        self.states.isActive.register(self.dock.toolButtonIsActive, "setChecked", bool)
        self.states.isActive.register(self.hud.toolButtonIsActive, "setChecked", bool)
        self.states.isActive.register(self.hud.toolButtonTMS, "setChecked", bool)
        self.states.isActive.register(self.hud.sliderZoomlevels, "setVisible", bool)
        self.states.isActive.register(self.dock.groupBoxZoomlevels, "setVisible", bool)
        self.states.isActive.register(self.hud, "setIsActive", bool)
        self.canvasAdapter.isActiveChanged.connect(self.storeStatus)
        self.canvasAdapter.isActiveChanged.connect(self.states.isActive.setValue)
        self.canvasAdapter.isActiveChanged.connect(self._updateCheckedComponents)
        self.dock.toolButtonIsActive.toggled.connect(self.canvasAdapter.setIsActive)
        self.hud.toolButtonIsActive.toggled.connect(self.canvasAdapter.setIsActive)
        self.hud.toolButtonTMS.toggled.connect(self.canvasAdapter.setIsActive)

        # menu TMS
        self.menuTMS = QtGui.QMenu(self.canvas)
        self.hud.toolButtonTMS.setMenu(self.menuTMS)
        self.menuTMS.addAction(self.dock.actionLayers)
        self.menuTMS.addAction(self.dock.actionHUD)
        self.menuTMS.addAction(self.dock.actionTMS)
        self.iface.addToolBarWidget(self.hud.toolButtonTMS)

        self.iface.addPluginToWebMenu(self._pluginName, self.dock.actionLayers)
        self.iface.addPluginToWebMenu(self._pluginName, self.dock.actionHUD)
        self.iface.addPluginToWebMenu(self._pluginName, self.dock.actionTMS)

        # menu layers
        self.menuLayers = QtGui.QMenu(self.canvas)
        self.hud.toolButtonLayers.setMenu(self.menuLayers)
        self.dock.toolButtonLayers.setMenu(self.menuLayers)
        self.dock.actionLayers.setMenu(self.menuLayers)
        self.hud.toolButtonLayers.clicked.connect(self.hud.toolButtonLayers.showMenu)
        self.dock.toolButtonLayers.clicked.connect(self.dock.toolButtonLayers.showMenu)

        # dpi
        self.states.dpi.register(self.dock.dpiSpinBox, "setValue", int)
        self.canvasAdapter.dpiChanged.connect(self.states.dpi.setValue)
        self.dock.toggleDpiToolButton.toggled.connect(self.switchIsActiveIcon)
        self.dock.dpiSpinBox.valueChanged.connect(self.canvasAdapter.setDpi)
        self.dock.resetDpiToolButton.clicked.connect(self.canvasAdapter.resetDpi)

        # coordinateReferenceSystems
        self.dock.checkBoxUseMercator.stateChanged.connect(self.useMercator)
        self.dock.checkBoxUseOnTheFlyTransformation.stateChanged.connect(self.canvas.mapRenderer().setProjectionsEnabled)

        # load datasets and create layer menu's
        self.dock.buttonLoadRefreshUserDatasets.clicked.connect(self.initUserDatasets)
        self.initUserDatasets()

        # initially update all components
        self.states.update()
        # set icon to all checkable components
        self._updateCheckedComponents()

    def _updateCheckedComponents(self):
        """set icon to all checkable components"""
        for component in [
            self.hud.toolButtonIsActive,
            self.dock.toolButtonIsActive,
            self.dock.actionHUD, 
            self.dock.actionTMS,
            self.dock.toggleDpiToolButton,
            self.hud.toolButtonTMS
        ]:
            self.changeIconColor(component, component.isChecked())

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(self._pluginName, self.dock.actionLayers)
        self.iface.removePluginMenu(self._pluginName, self.dock.actionHUD)
        self.iface.removePluginMenu(self._pluginName, self.dock.actionTMS)

        self.iface.removeToolBarIcon(self.dock.actionTMS)
        self.iface.removeToolBarIcon(self.dock.actionHUD)
        self.iface.removeDockWidget(self.dock)
        del self.dock
        self.hud.frameButtons.setParent(None)
        self.hud.toolButtonTMS.setParent(None)
        del self.hud

    def switchIsActiveIcon(self, checked):
        self.changeIconColor(self.sender(), checked)

    def changeIconColor(self, component, checked, iconSize=22):
        """Change icon color to red if not checked and to green if checked

        Args:
            component (QObject): QObject to set icon.
        """
        name = component.objectName()

        path = ":/icons/icons/{0}.svg".format(name)
        f = QFile(path)
        if f.open(QFile.ReadOnly | QFile.Text):
            textStream = QTextStream(f)
            svgData = textStream.readAll()
            f.close()

            if checked:
                svgData = svgData.replace(FLAT_BLUE, FLAT_GREEN)
            else:
                svgData = svgData.replace(FLAT_BLUE, FLAT_RED)

            svg = QSvgRenderer(QByteArray(svgData))
            image = QImage(iconSize, iconSize, QImage.Format_ARGB32)
            image.fill(0)
            painter = QPainter()
            painter.begin(image)
            svg.render(painter)
            painter.end()
            pixmap = QPixmap.fromImage(image)
            icon = QIcon(pixmap)
            component.setIcon(icon)
        else:
            raise IOError, "Can't open path: {0}".format(path)

    def showInfo(self):
        self.dialogInfo = DialogInfo(self.workingDir)
        self.dialogInfo.setParent(self.iface.mainWindow(), self.dialogInfo.windowFlags())
        self.dialogInfo.exec_() 

    def initUserDatasets(self):
        filenames = os.listdir(self.datasetDir)
        filenames.sort()

        for action in self._actions:
            self.menuLayers.removeAction(action)
            action.setParent(None)
            del action

        for filename in filenames:
            if 'aux' in filename: continue
            if filename.endswith('.xml'):
                action = QAction(self._getMapIcon(filename), filename, self.dock)
                action.setObjectName(filename)
                action.triggered.connect(self.loadSelectedUserDataset)
                self._actions.append(action)
                self.menuLayers.addAction(action)

    def _getMapIcon(self, filename):
        if any(word in filename for word in ["osm", "openstreetmap"]):
            return QIcon(":/icons/icons/osm.svg")
        elif "google" in filename:
            return QIcon(":/icons/icons/google.svg")
        elif "bing" in filename:
            return QIcon(":/icons/icons/bing.svg")
        elif "mapbox" in filename:
            return QIcon(":/icons/icons/mapbox.svg")
        else:
            return QIcon(":/icons/icons/map.png")

    def loadSelectedUserDataset(self):
        selectedDataset = self.sender().objectName()
        datasetPath = os.path.join(self.datasetDir, selectedDataset)
        errorMessage = "Unable to load file %s" % datasetPath
        if (selectedDataset == ""):
            self.iface.messageBar().pushMessage("Error", errorMessage, QgsMessageBar.CRITICAL)
        elif os.path.exists(datasetPath):
            self.iface.addRasterLayer(datasetPath, selectedDataset)
        else:
            self.iface.messageBar().pushMessage("Error", errorMessage, QgsMessageBar.CRITICAL)

    def useMercator(self, checked):
        if checked:
            coordinateReferenceSystem = QgsCoordinateReferenceSystem()
            createCrs = coordinateReferenceSystem.createFromString("EPSG:3857")

            if self.projection != coordinateReferenceSystem:
                self.projection = self.canvas.mapRenderer().destinationCrs()

            self.canvas.mapRenderer().setDestinationCrs(coordinateReferenceSystem)

    def storeStatus(self, checked):
        s = QSettings()
        s.setValue("tilemapscalelevels/active", checked)

    def readStatus(self):
        s = QSettings()
        isActive = s.value("tilemapscalelevels/active", True, type=bool)
        return isActive

class HUD(QWidget, Ui_hud):

    spacing = 6

    def __init__(self, canvas, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        self._isActive = True

        self.frameButtons.setParent(canvas)
        self._placeFrame()
        self.updateGeometry()
        self.frameButtons.show()

    def _placeFrame(self):
        self.frameButtons.move(self.spacing, self.spacing)

    def updateGeometry(self):
        if self._isActive:
            self.frameButtons.resize(self.frameButtons.width(), 261)
        else:
            self.frameButtons.resize(self.frameButtons.width(), 81)

    def isActive(self):
        return self._isActive

    def setIsActive(self, isActive):
        self._isActive = isActive
        self.updateGeometry()

class DialogInfo(QDialog, Ui_info):

    def __init__(self, workingDir, infoHtml="README.html"):
        super(DialogInfo, self).__init__()
        self.setupUi(self)
        self.resize(1280, 768)

        self.workingDir = workingDir
        self.infoHtml = infoHtml
        self.goHome()
        self.buttonHome.clicked.connect(self.goHome)

    def goHome(self):
        url = os.path.join(self.workingDir, self.infoHtml)
        self.webView.setUrl(QUrl(url))