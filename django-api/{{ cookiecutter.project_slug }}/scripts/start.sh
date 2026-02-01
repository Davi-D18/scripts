#!/usr/bin/env bash
set -e

# Detecta se o poetry está instalado e monta o comando base em array
if command -v poetry >/dev/null 2>&1; then
  PY_CMD=(poetry run python)
  echo "ℹ️ Poetry encontrado — usando: ${PY_CMD[*]}"
else
  PY_CMD=(python)
  echo "ℹ️ Poetry não encontrado — usando: ${PY_CMD[*]}"
fi

# 1. Migrações (aplica apenas pendentes)
echo "🔄 Aplicando migrations..."
"${PY_CMD[@]}" manage.py migrate --noinput

# 2. Variável para o diretório de estáticos
STATIC_DIR="staticfiles"
# 2a. Arquivo de exemplo para testar existência de estáticos do Admin
CHECK_FILE="$STATIC_DIR/admin/css/base.css"

# 3. Se o diretório não existir, ou estiver vazio, ou faltar o arquivo CHECK_FILE, roda collectstatic
if [ ! -d "$STATIC_DIR" ] \
   || [ -z "$(ls -A -- "$STATIC_DIR")" ] \
   || [ ! -f "$CHECK_FILE" ]; then

  echo "📦 Coletando arquivos estáticos..."
  "${PY_CMD[@]}" manage.py collectstatic --noinput

else
  echo "✅ Arquivos estáticos já coletados, pulando collectstatic."
fi

# 4. Aplicar seeders no banco de dados
if [ -d "seeders" ] && [ "$(ls -A seeders 2>/dev/null)" ]; then
  echo "🌱 Aplicando seeders..."
  "${PY_CMD[@]}" manage.py shell -c 'from django.core.management import call_command
try:
    call_command("seeder", "--all")
    print("✅ Seeders aplicados com sucesso!")
except Exception as e:
    print(f"⚠️ Erro ao aplicar seeders: {e}")'
else
  echo "ℹ️ Pasta seeders não encontrada ou vazia, pulando seeders."
fi

# 5. Criar superusuário a partir das variáveis de ambiente
echo "👤 Verificando superusuário..."
"${PY_CMD[@]}" manage.py shell -c 'import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
if username and email and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Superusuário {username} criado com sucesso!")
    else:
        print(f"ℹ️ Superusuário {username} já existe.")
else:
    print("⚠️ Variáveis de ambiente para superusuário não definidas.")'

# 6. Inicia o Gunicorn na porta definida pelo Render (rodando dentro do mesmo ambiente)
echo "🚀 Iniciando Gunicorn..."
PORT=${PORT:-8000}
exec "${PY_CMD[@]}" -m gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
