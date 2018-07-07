#!/bin/bash

set -e

pip install "setuptools>=38.6.0"
pip install "twine>=1.11.0"
python setup.py sdist
