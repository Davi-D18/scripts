.PHONY: install format lint migrate run
{%- if cookiecutter.use_tests == "yes" %}
.PHONY: test
{%- endif %}
{%- if cookiecutter.use_tailwind == "yes" %}
.PHONY: tailwind tailwind-watch
{%- endif %}
{%- if cookiecutter.use_docker == "yes" %}
.PHONY: docker-build docker-up
{%- endif %}

{% if cookiecutter.dependency_manager == "poetry" -%}
install:
	poetry install

run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

format:
	poetry run ruff format .
	poetry run ruff check --fix .

lint:
	poetry run ruff check .
{%- if cookiecutter.use_tests == "yes" %}

test:
	poetry run pytest
{%- endif %}
{%- else -%}
install:
	pip install -r requirements-dev.txt

run:
	python manage.py runserver

migrate:
	python manage.py migrate

format:
	ruff format .
	ruff check --fix .

lint:
	ruff check .
{%- if cookiecutter.use_tests == "yes" %}

test:
	pytest
{%- endif %}
{%- endif %}
{%- if cookiecutter.use_tailwind == "yes" %}

tailwind:
	npm install
	npm run build

tailwind-watch:
	npm run watch
{%- endif %}
{%- if cookiecutter.use_docker == "yes" %}

docker-build:
	docker compose build

docker-up:
	docker compose up --build
{%- endif %}
