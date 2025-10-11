.PHONY: install-dev format lint test commit-install pre-commit update

install-dev:
	pip install -r requirements_dev.txt

format:
	black .
	isort .

lint:
	flake8 .

test:
	pytest

commit-install:
	pre-commit install

commit-upgrade:
	pre-commit update