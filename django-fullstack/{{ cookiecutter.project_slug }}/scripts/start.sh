#!/usr/bin/env bash
set -e

# Detecta o gerenciador (poetry, se disponível)
if command -v poetry >/dev/null 2>&1; then
  PY_CMD=(poetry run python)
  echo "Poetry encontrado - usando: ${PY_CMD[*]}"
else
  PY_CMD=(python)
  echo "Poetry nao encontrado - usando: ${PY_CMD[*]}"
fi

# 1. Migrations
echo "Aplicando migrations..."
"${PY_CMD[@]}" manage.py migrate --noinput

# 2. Estaticos
STATIC_DIR="staticfiles"
CHECK_FILE="$STATIC_DIR/admin/css/base.css"
if [ ! -d "$STATIC_DIR" ] || [ -z "$(ls -A -- "$STATIC_DIR")" ] || [ ! -f "$CHECK_FILE" ]; then
  echo "Coletando arquivos estaticos..."
  "${PY_CMD[@]}" manage.py collectstatic --noinput
else
  echo "Arquivos estaticos ja coletados."
fi

# 3. Seeders
if [ -d "seeders" ] && [ "$(ls -A seeders 2>/dev/null)" ]; then
  echo "Aplicando seeders..."
  "${PY_CMD[@]}" manage.py shell -c 'from django.core.management import call_command
try:
    call_command("seeder", "--all")
    print("Seeders aplicados com sucesso!")
except Exception as e:
    print(f"Erro ao aplicar seeders: {e}")'
else
  echo "Pasta seeders vazia, pulando seeders."
fi

# 4. Superusuario (via variaveis de ambiente)
echo "Verificando superusuario..."
"${PY_CMD[@]}" manage.py shell -c 'import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
if username and email and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superusuario {username} criado.")
    else:
        print(f"Superusuario {username} ja existe.")
else:
    print("Variaveis de superusuario nao definidas.")'

# 5. Uvicorn (WSGI por padrão; troque para core.asgi:application para ASGI)
echo "Iniciando Uvicorn..."
PORT=${PORT:-8000}
exec "${PY_CMD[@]}" -m uvicorn core.wsgi:application --interface wsgi --host 0.0.0.0 --port $PORT
