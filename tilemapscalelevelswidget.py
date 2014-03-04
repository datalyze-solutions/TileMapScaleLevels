from ui_tilemapscalelevelswidget import Ui_TileMapScaleLevelsDockWidget
from PyQt4 import QtGui

class TileMapScaleLevelsDockWidget(QtGui.QDockWidget, Ui_TileMapScaleLevelsDockWidget):

    def __init__(self):
        super(TileMapScaleLevelsDockWidget, self).__init__()
        
        self.setupUi(self)
        self.show()