.PHONY: format lint test commit-install pre-commit update

{%- if cookiecutter.use_poetry == "yes" %}
format:
	poetry run black .
	poetry run isort .

lint:
	poetry run flake8 .

test:
	poetry run pytest

commit-install:
	poetry run pre-commit install

commit-upgrade:
	poetry run pre-commit update
{%- endif %}
{%- if cookiecutter.use_poetry == "no" %}
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
{%- endif %}
