#!/usr/bin/env bash

# Força o Python a usar UTF-8 em todo o I/O
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

# Repasse todos os argumentos para manage.py
{%- if cookiecutter.dependency_manager == "poetry" %}
poetry run python -X utf8 manage.py "$@"
{%- else %}
python -X utf8 manage.py "$@"
{%- endif %}
