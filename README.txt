Tile Map Scale Plugin
---------------------

Functionality
-------------
    Most webmaps like OpenStreetMap, Bing, Google, Yahoo, etc. are rendered for specific scales. If they are
    viewed with a different scale, they appear fuzzy and unsharp. If activated this plugin sets the scale to
    the next matching scale while zooming in or out.

Own datasets
------------
    The plugin is able to load datasets based on the
    <a href="http://www.gdal.org/frmt_wms.html">GDAL WMS Driver</a>. You can add your own
    datasets by creating an XML file in the "datasets" folder. The datasets folder is located in the
    default plugin folder. Normaly the plugin directory is located in
    "your user directory"/.qgis/python/plugins/TileMapScalePlugin/. After adding the file
    press the "refresh" button or restart QGIS to be able to load your file from the dropdown list.

Links
-----
    You found a bug? You want to contribute with code or ideas? Contact us on
    http://github.com/datalyze-solutions/TileMapScaleLevels