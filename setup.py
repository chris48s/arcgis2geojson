from setuptools import setup
import io
import os

def _get_description():
    try:
        path = os.path.join(os.path.dirname(__file__), 'README.md')
        with io.open(path, encoding='utf-8') as f:
            return f.read()
    except IOError:
        return ''

setup(
    name='arcgis2geojson',
    description='A Python library for converting ArcGIS JSON to GeoJSON',
    long_description=_get_description(),
    long_description_content_type="text/markdown",
    version='1.5.0',
    author="chris48s",
    license="MIT",
    url="https://github.com/chris48s/arcgis2geojson/",
    install_requires=['six'],
    extras_require={
        'testing': [
            'python-coveralls',
            'mock',
        ]
    },
    py_modules=['arcgis2geojson'],
    entry_points={
        'console_scripts': [
            'arcgis2geojson = arcgis2geojson:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
