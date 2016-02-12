# -*- coding: utf-8 -*-
import math

class TileMapServiceCalculator(object):

    def __init__(self, maxZoomlevel=30, minZoomlevel=0, dpi=96, tileSize=256, earthRadius=6378137):
        """calculator to transform zoomlevels to scale and back again

        Hint:
            Remember, that we use the global mercator reference system and distances are not the "real" distance, except on the equator!
            Stuff to read:
            * https://msdn.microsoft.com/en-us/library/aa940990.aspx
            * https://msdn.microsoft.com/en-us/library/bb259689.aspx

        Attributes:
            _inchesPerMeter (float): Defaults to 39.37.
            _maxScalePerPixel (float): Maximum size of a pixel in zoomlevel 0 in m. Defaults to 156543.03392804097

        Args:
            maxZoomlevel (int, optional): Maximum available zoomlevel. Defaults to 30.
            minZoomlevel (int, optional): Minimum available zoomlevel. Defaults to 0.
            dpi (int, optional): DPI settings to use for calculation. Use the exact DPI setting of your screen! Defaults to 96.
            tileSize (int, optional): Pixelsize of a tile. Defaults to 256.
            earthRadius (float, optional): Earth radius in meters to use. Defaults to 6378137.
        """
        self._dpi = dpi
        self._inchesPerMeter = 39.37
        self._maxScalePerPixel = 156543.03392804097
        self._earthRadius = earthRadius
        self._tileSize = tileSize
        self._maxZoomlevel = 0
        self._minZoomlevel = 30
        self._minScale = 1
        self._maxScale = 1000000000
        self.setMinZoomlevel(minZoomlevel)
        self.setMaxZoomlevel(maxZoomlevel)

        self.processedScales = {}
        self.calculateScaleStorage()

    def minZoomlevel(self):
        """return minimum available zoomlevel"""
        return self._minZoomlevel

    def setMinZoomlevel(self, zoomlevel):
        """set minimum available zoomlevel

        Args:
            minZoomlevel (int, >=0): If zoomlevel is smaller than 0 its set to 0.
        """
        if zoomlevel >= 0:            
            self._minZoomlevel = zoomlevel
        else:
            self._minZoomlevel = 0
        self._minScale = self.getScale(self._minZoomlevel)
        
    def minScale(self):
        """get minimum possible scale depending on maxZoomlevel"""
        return self._minScale

    def maxZoomlevel(self):
        """return maximum available zoomlevel"""
        return self._maxZoomlevel

    def setMaxZoomlevel(self, zoomlevel):
        """set maximum available zoomlevel

        Args:
            maxZoomlevel (int, >=0): If zoomlevel is smaller than minZoomlevel its set to minZoomlevel
        """
        if zoomlevel >= self._minZoomlevel:
            self._maxZoomlevel = zoomlevel
        else:
            self._maxZoomlevel = self._minZoomlevel
        self._maxScale = self.getScale(self._maxZoomlevel)

    def maxScale(self):
        """get maximum possible scale depending on maxZoomlevel"""
        return self._maxScale

    def dpi(self):
        """return screen dpi"""
        return self._dpi

    def setDpi(self, dpi):
        """set the screen dpi for calculation

        Args:
            dpi (int)
        """
        self._dpi = dpi
        self.calculateScaleStorage()

    def resetDpi(self):
        """reset dpi to screen defaults"""
        self.setDpi(TileMapServiceCalculator.askForScreenDpi())

    @staticmethod
    def askForScreenDpi():
        """use Qt to return the screen dpi

        Raises:
            ImportError if Qt is not installed
        """
        try:
            from PyQt4 import QtGui
            return QtGui.QMainWindow().physicalDpiX()
        except ImportError as e:
            raise e, "Qt not installed"
        except:
            raise

    def getScale(self, zoomlevel):
        try:
            zoomlevel = int(zoomlevel)
            scale = int((self._dpi * self._inchesPerMeter * self._maxScalePerPixel) / (math.pow(2, zoomlevel)))
            return scale
        except TypeError:
            raise
        except Exception as e:
            raise e

    def getZoomlevel(self, scale):
        """get a zoomlevel from scale"""
        if scale > 0:
            scale = int(scale)
            if scale not in self.processedScales:
                zoomlevel = int(round(math.log( ((self._dpi * self._inchesPerMeter * self._maxScalePerPixel) / scale), 2 ), 0))
                self.processedScales[scale] = zoomlevel
                if zoomlevel > self.maxZoomlevel():
                    return self.maxZoomlevel()
                elif zoomlevel <= self.minZoomlevel():
                    return self.minZoomlevel()
                else:
                    return zoomlevel
            else:
                zoomlevel = self.processedScales[scale]
                return zoomlevel

    def mapWidth(self, zoomlevel):
        """width of the map for a zoomlevel in pixels"""
        return self._tileSize * math.pow(2, zoomlevel)

    def pixelSize(self, zoomlevel):
        """calculate the size of a pixel in a zoomlevel"""
        return 2.0 * math.pi * self._earthRadius / self.mapWidth(zoomlevel)

    def calculateScaleStorage(self):
        """pre calculate a scale-zoomlevel key storage for faster lookup"""
        for zoomlevel in xrange(self.minZoomlevel(), self.maxZoomlevel()):
            self.processedScales[self.getScale(zoomlevel)] = zoomlevel 
