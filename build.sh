#!/bin/bash

set -e

pandoc --from=markdown --to=rst --output=README.rst README.md
python setup.py sdist
