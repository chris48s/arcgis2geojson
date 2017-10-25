from distutils.core import setup
import os

def _get_description():
    try:
        path = os.path.join(os.path.dirname(__file__), 'README.rst')
        with open(path, encoding='utf-8') as f:
            return f.read()
    except IOError:
        return ''

setup(
    name='arcgis2geojson',
    description='A Python library for converting ArcGIS JSON to GeoJSON',
    long_description=_get_description(),
    version='1.0.2',
    author="chris48s",
    license="MIT",
    url="https://github.com/chris48s/arcgis2geojson/",
    py_modules=['arcgis2geojson'],
)
