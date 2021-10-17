SHELL := /bin/bash
.PHONY: help format install lint test release

help:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

format:
	poetry run isort --profile black .
	poetry run black .

install:
	poetry install

lint:
	poetry run isort --profile black -c --diff .
	poetry run black --check .
	poetry run flake8 .

test:
	poetry run coverage run --source=arcgis2geojson ./run_tests.py
	poetry run coverage xml

release:
	# usage: `make release version=0.0.0`
	make test
	@echo ""
	make lint
	@echo ""
	./release.sh "$(version)"
