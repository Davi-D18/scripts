# syntax=docker/dockerfile:1
{%- if cookiecutter.use_tailwind == "yes" %}

# ---------- frontend (Tailwind) ----------
FROM node:20-alpine AS frontend
WORKDIR /app
COPY package.json ./
RUN npm install
COPY tailwind.config.js ./
COPY . .
RUN npm run build
{%- endif %}

# ---------- runtime ----------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_ENV=production

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
{%- if cookiecutter.database == "postgresql" %}
    libpq-dev gcc \
{%- elif cookiecutter.database == "mysql" %}
    default-libmysqlclient-dev pkg-config gcc \
{%- else %}
    gcc \
{%- endif %}
    && rm -rf /var/lib/apt/lists/*

{%- if cookiecutter.dependency_manager == "poetry" %}
RUN pip install --no-cache-dir "poetry>=2.0.0"
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-root
{%- else %}
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
{%- endif %}

COPY . .
{%- if cookiecutter.use_tailwind == "yes" %}
COPY --from=frontend /app/static/css/main.css ./static/css/main.css
{%- endif %}

RUN chmod +x scripts/*.sh

# SECRET_KEY apenas para o collectstatic em build; sobrescrita em runtime
RUN DJANGO_SECRET_KEY=build-only-secret python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["./scripts/entrypoint.sh"]
