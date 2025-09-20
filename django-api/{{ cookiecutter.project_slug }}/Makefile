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

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/