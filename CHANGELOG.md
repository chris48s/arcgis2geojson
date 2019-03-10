# Changelog

## :package: [1.5.0](https://pypi.python.org/pypi/arcgis2geojson/1.5.0) - 2019-03-10

* Add CLI wrapper

## :package: [1.4.0](https://pypi.python.org/pypi/arcgis2geojson/1.4.0) - 2018-11-09

* Support Python 3.7, drop testing on 3.2, 3.3

## :package: [1.3.0](https://pypi.python.org/pypi/arcgis2geojson/1.3.0) - 2018-07-07

* Convert ArcGIS `Extent` to GeoJSON `Polygon`

## :package: [1.2.0](https://pypi.python.org/pypi/arcgis2geojson/1.2.0) - 2018-03-30

* Convert ArcGIS `features` array to GeoJSON `FeatureCollection`
* Convert dict to dict or json to json:
    * `arcgis2geojson("{}")` returns string
    * `arcgis2geojson({})` returns dict

## :package: [1.1.1](https://pypi.python.org/pypi/arcgis2geojson/1.1.1) - 2018-02-28

Bugfix: Require `six` in setup.py

## :package: [1.1.0](https://pypi.python.org/pypi/arcgis2geojson/1.1.0) - 2018-02-26

Improve compliance with RFC 7946:

* Wind outer rings counterclockwise and inner rings clockwise
* Prevent values other than string or number in id field
* Convert but log a warning if input SRID is not 4326

## :package: [1.0.4](https://pypi.python.org/pypi/arcgis2geojson/1.0.4) - 2017-12-29

Bugfix: Preserve Z-values if present in input geometry

## :package: [1.0.3](https://pypi.python.org/pypi/arcgis2geojson/1.0.3) - 2017-10-26

Bugfix: Fix install under python 2.7

## :package: [1.0.2](https://pypi.python.org/pypi/arcgis2geojson/1.0.2) - 2017-10-25

Distribute via PyPI

## :package: 1.0.1 - 2017-07-21

Bugfix: If geometry is empty or invalid, return None

## :package: 1.0.0 - 2017-01-10

First Release
