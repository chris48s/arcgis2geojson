# Changelog

## 📦 [3.1.1](https://pypi.python.org/pypi/arcgis2geojson/3.1.1) - 2025-10-22

* Fix build build-backend declaration

## 📦 [3.1.0](https://pypi.python.org/pypi/arcgis2geojson/3.1.0) - 2025-10-11

* Dropped testing on python < 3.10
* Tested on python 3.13, 3.14

## 📦 [3.0.3](https://pypi.python.org/pypi/arcgis2geojson/3.0.3) - 2024-07-09

* Don't use the root logger

## 📦 [3.0.2](https://pypi.python.org/pypi/arcgis2geojson/3.0.2) - 2023-10-08

* Tested on python 3.11, 3.12

## 📦 [3.0.1](https://pypi.python.org/pypi/arcgis2geojson/3.0.1) - 2021-11-07

* Log a warning if geometry can not be converted

## 📦 [3.0.0](https://pypi.python.org/pypi/arcgis2geojson/3.0.0) - 2021-10-17

* Dropped testing on python < 3.7
* Tested on python 3.9, 3.10

## 📦 [2.0.1](https://pypi.python.org/pypi/arcgis2geojson/2.0.1) - 2020-12-06

* CLI: show help and exit if called interactively with no args

## 📦 [2.0.0](https://pypi.python.org/pypi/arcgis2geojson/2.0.0) - 2020-01-19

* Breaking: Drop python 2.7 compatibility

## 📦 [1.5.0](https://pypi.python.org/pypi/arcgis2geojson/1.5.0) - 2019-03-10

* Add CLI wrapper

## 📦 [1.4.0](https://pypi.python.org/pypi/arcgis2geojson/1.4.0) - 2018-11-09

* Support Python 3.7, drop testing on 3.2, 3.3

## 📦 [1.3.0](https://pypi.python.org/pypi/arcgis2geojson/1.3.0) - 2018-07-07

* Convert ArcGIS `Extent` to GeoJSON `Polygon`

## 📦 [1.2.0](https://pypi.python.org/pypi/arcgis2geojson/1.2.0) - 2018-03-30

* Convert ArcGIS `features` array to GeoJSON `FeatureCollection`
* Convert dict to dict or json to json:
    * `arcgis2geojson("{}")` returns string
    * `arcgis2geojson({})` returns dict

## 📦 [1.1.1](https://pypi.python.org/pypi/arcgis2geojson/1.1.1) - 2018-02-28

Bugfix: Require `six` in setup.py

## 📦 [1.1.0](https://pypi.python.org/pypi/arcgis2geojson/1.1.0) - 2018-02-26

Improve compliance with RFC 7946:

* Wind outer rings counterclockwise and inner rings clockwise
* Prevent values other than string or number in id field
* Convert but log a warning if input SRID is not 4326

## 📦 [1.0.4](https://pypi.python.org/pypi/arcgis2geojson/1.0.4) - 2017-12-29

Bugfix: Preserve Z-values if present in input geometry

## 📦 [1.0.3](https://pypi.python.org/pypi/arcgis2geojson/1.0.3) - 2017-10-26

Bugfix: Fix install under python 2.7

## 📦 [1.0.2](https://pypi.python.org/pypi/arcgis2geojson/1.0.2) - 2017-10-25

Distribute via PyPI

## 📦 1.0.1 - 2017-07-21

Bugfix: If geometry is empty or invalid, return None

## 📦 1.0.0 - 2017-01-10

First Release
