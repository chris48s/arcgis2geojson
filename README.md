# arcgis2geojson.py
A Python library for converting ArcGIS JSON to GeoJSON: A partial port of ESRI's [arcgis-to-geojson-utils](https://github.com/Esri/arcgis-to-geojson-utils/).

## Platform Support
arcgis2geojson is tested under python versions 2.7, 3.2, 3.3, 3.4 and 3.5

## Usage

```
>>> input = {
...     'attributes': {'OBJECTID': 123},
...     'geometry': {   'rings': [   [   [41.8359375, 71.015625],
...                                      [56.953125, 33.75],
...                                      [21.796875, 36.5625],
...                                      [41.8359375, 71.015625]]],
...                     'spatialReference': {'wkid': 4326}}}
>>> from arcgis2geojson import arcgis2geojson
>>> output = arcgis2geojson(input)
>>> import pprint
>>> pp = pprint.PrettyPrinter(indent=4)
>>> pp.pprint(output)
{   'geometry': {   'coordinates': [   [   [41.8359375, 71.015625],
                                           [56.953125, 33.75],
                                           [21.796875, 36.5625],
                                           [41.8359375, 71.015625]]],
                    'type': 'Polygon'},
    'id': 123,
    'properties': {'OBJECTID': 123},
    'type': 'Feature'}
```

## Licensing

arcgis2geojson is a derivative work of ESRI's [arcgis-to-geojson-utils](https://github.com/Esri/arcgis-to-geojson-utils/). Original code is Copyright 2015 by Esri and was licensed under [the Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

arcgis2geojson is made available under the MIT License.
