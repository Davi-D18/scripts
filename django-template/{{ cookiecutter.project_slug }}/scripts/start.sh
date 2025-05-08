#!/usr/bin/env bash
set -e

# 1. Migrações (aplica apenas pendentes)
echo "🔄 Aplicando migrations..."
python manage.py migrate --noinput

# 2. Variável para o diretório de estáticos
STATIC_DIR="staticfiles"
# 2a. Arquivo de exemplo para testar existência de estáticos do Admin
CHECK_FILE="$STATIC_DIR/admin/css/base.css"

# 3. Se o diretório não existir, ou estiver vazio, ou faltar o arquivo CHECK_FILE, roda collectstatic
if [ ! -d "$STATIC_DIR" ] \
   || [ -z "$(ls -A -- "$STATIC_DIR")" ] \
   || [ ! -f "$CHECK_FILE" ]; then

  echo "📦 Coletando arquivos estáticos..."
  python manage.py collectstatic --noinput

else
  echo "✅ Arquivos estáticos já coletados, pulando collectstatic."
fi

# 4. Inicia o Gunicorn na porta definida pelo Render
echo "🚀 Iniciando Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT

