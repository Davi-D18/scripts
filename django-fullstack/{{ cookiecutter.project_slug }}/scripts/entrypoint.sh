#!/usr/bin/env sh
set -e

echo "Aplicando migrations..."
python manage.py migrate --noinput

echo "Coletando arquivos estaticos..."
python manage.py collectstatic --noinput

echo "Iniciando Uvicorn (WSGI)..."
exec python -m uvicorn core.wsgi:application --interface wsgi --host 0.0.0.0 --port 8000
