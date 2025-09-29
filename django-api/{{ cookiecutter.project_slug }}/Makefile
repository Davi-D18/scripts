.PHONY: install-dev format lint test

install-dev:
	pip install -r requirements_dev.txt

format:
	black .
	isort .

lint:
	flake8 .

test:
	pytest