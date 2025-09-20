.PHONY: install-dev format lint test clean

install-dev:
	pip install -r requirements-dev.txt

format:
	black .
	isort .

lint:
	flake8 .

test:
	pytest