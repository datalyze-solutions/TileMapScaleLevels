# -*- coding: utf-8 -*-
try:
    from tms.calculator import TileMapServiceCalculator
except ImportError:
    from calculator import TileMapServiceCalculator

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot as Slot, pyqtSignal as Signal
from qgis.gui import (
    QgsMapCanvas
)

class TileMapServiceCanvasAdapter(QtCore.QObject):

    zoomlevelChanged = Signal(int)
    minZoomlevelChanged = Signal(int)
    maxZoomlevelChanged = Signal(int)
    isActiveChanged = Signal(bool)
    dpiChanged = Signal(int)

    def __init__(self, canvas, minZoomlevel=0, maxZoomlevel=18):
        super(QtCore.QObject, self).__init__(None)
        """"Adapter to apply zoom updates to canvas

        Args:
            canvas (QgsMapCanvas): canvas to use.
            minZoomlevel (int): minimum zoomlevel of map, optional, defaults to 0.
            maxZoomlevel (int): maximum zoomlevel of map, < minZoomlevel, optional, defaults to 18.
            zoomlevelChanged (QtCore.pyqtSignal): Emitted after the scale changed and a new zoomlevel was set.

        """
        self._canvas = canvas
        self._scaleCalculator = TileMapServiceCalculator(
            maxZoomlevel=18,
            minZoomlevel=0,
            dpi=canvas.mapSettings().outputDpi()
        )

        self._canvas.extentsChanged.connect(self.adaptToTms)
        self._lastZoomlevel = 0
        self._isActive = True

    @Slot()
    def adaptToTms(self):
        """Calculate the new extent and zoomlevel if canvas was created with useTmsScales.

        Hint:
            If you want default qgis zoom behavior create the canvas without useTmsScales or
            disconnect self.extentsChanged.disconnect(self.adaptScaleToTms)
        """
        if self._isActive:
            # disable all signals and stop rendering
            self._canvas.setRenderFlag(False)
            self._canvas.blockSignals(True)

            scale = self._canvas.scale()
            zoomlevel = self._scaleCalculator.getZoomlevel(self._canvas.scale())

            # update zoom behavior
            if zoomlevel > self.minZoomlevel() and zoomlevel < self.maxZoomlevel():
                self._canvas.setWheelAction(QgsMapCanvas.WheelZoomToMouseCursor, 2)
            else:
                self._canvas.setWheelAction(QgsMapCanvas.WheelZoom, 2)

            # update scale
            if scale <= self.minScale() and scale >= self.maxScale():
                newScale = self._scaleCalculator.getScale(zoomlevel)
                self._canvas.zoomScale(newScale)
            else:
                if scale > self.minScale():
                    self._canvas.zoomScale(self.minScale())
                else:
                    self._canvas.zoomScale(self.maxScale())

            # reactivate disabled signals and rendering
            self._canvas.setRenderFlag(True)
            self._canvas.blockSignals(False)

            # inform other components
            self.zoomlevelChanged.emit(zoomlevel)

    def zoomZoomlevel(self, zoomlevel):
        """zoom with zoomlevel

        Args:
            zoomlevel (int): Zoom to this zoomlevel. Has to be in range of min/maxZoomlevel.

        """
        print zoomlevel
        if zoomlevel != self._lastZoomlevel:
            self._lastZoomlevel = zoomlevel

            newScale = self._scaleCalculator.getScale(zoomlevel)
            self._canvas.zoomScale(newScale)
            self.adaptToTms()

    def zoomlevel(self):
        """return current zoomlevel"""
        zoomlevel = self._scaleCalculator.getZoomlevel(self._canvas.scale())

    def minZoomlevel(self):
        """return the minimum available zoomlevel"""
        return self._scaleCalculator.minZoomlevel()

    def setMinZoomlevel(self, zoomlevel):
        """set minimum available zoomlevel

        Args:
            minZoomlevel (int, >=0)
        """
        self._scaleCalculator.setMinZoomlevel(zoomlevel)
        self.minZoomlevelChanged.emit(zoomlevel)

    def minScale(self):
        """get minimum possible scale depending on maxZoomlevel"""
        return self._scaleCalculator.minScale()

    def maxZoomlevel(self):
        """return the maximum available zoomlevel"""
        return self._scaleCalculator.maxZoomlevel()

    def setMaxZoomlevel(self, zoomlevel):
        """set maximum available zoomlevel

        Args:
            maxZoomlevel (int, >=0)
        """
        self._scaleCalculator.setMaxZoomlevel(zoomlevel)
        self.maxZoomlevelChanged.emit(zoomlevel)

    def maxScale(self):
        """get maximum possible scale depending on maxZoomlevel"""
        return self._scaleCalculator.maxScale()

    def isActive(self):
        """Is scaling to TMS scales active or not"""
        return self._isActive

    def setIsActive(self, isActive):
        """set _isActive"""
        self._isActive = isActive
        self.isActiveChanged.emit(isActive)
        self.adaptToTms()

    def dpi(self):
        """get current screen dpi"""
        return self._scaleCalculator.dpi()

    def setDpi(self, dpi):
        """set dpi"""
        self._scaleCalculator.setDpi(dpi)
        self.dpiChanged.emit(dpi)
        self.adaptToTms()

    def resetDpi(self):
        """reset dpi setting to screen"""
        self.setDpi(self._scaleCalculator.askForScreenDpi())