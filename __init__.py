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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load TileMapScalePlugin class from file TileMapScalePlugin
    from tilemapscaleplugin import TileMapScalePlugin
    return TileMapScalePlugin(iface)
