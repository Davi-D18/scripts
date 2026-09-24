# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

Stack: Django + Django Template Language{% if cookiecutter.use_tailwind == "yes" %} + Tailwind CSS{% endif %}{% if cookiecutter.use_htmx == "yes" %} + HTMX{% endif %}.

## Requisitos

- Python 3.12+
{%- if cookiecutter.dependency_manager == "poetry" %}
- Poetry
{%- endif %}
{%- if cookiecutter.use_tailwind == "yes" %}
- Node.js 20+ (build do CSS)
{%- endif %}
{%- if cookiecutter.use_docker == "yes" %}
- Docker + Docker Compose
{%- endif %}

## Setup local

```bash
cp .env.example .env      # ajuste DJANGO_SECRET_KEY
```

Instale as dependências:

{% if cookiecutter.dependency_manager == "poetry" -%}
```bash
poetry install
```
{%- else -%}
```bash
pip install -r requirements-dev.txt
```
{%- endif %}

Prepare o banco e rode:

```bash
sh django.sh migrate
{%- if cookiecutter.use_tailwind == "yes" %}
make tailwind        # compila o CSS (use `make tailwind-watch` em desenvolvimento)
{%- endif %}
sh django.sh runserver
{%- if cookiecutter.use_authentication == "yes" %}
sh django.sh createsuperuser
{%- endif %}
```

Acesse http://localhost:8000/.

## Comandos

| Comando | Descrição |
|---------|-----------|
| `sh django.sh <cmd>` | Executa comandos Django (compatível com Windows) |
| `make format` / `make lint` | Ruff (formatação / verificação) |
{%- if cookiecutter.use_tests == "yes" %}
| `make test` | pytest |
{%- endif %}
{%- if cookiecutter.use_tailwind == "yes" %}
| `make tailwind` / `make tailwind-watch` | Compila o CSS |
{%- endif %}
{%- if cookiecutter.use_docker == "yes" %}
| `make docker-up` | Sobe com docker-compose |
{%- endif %}

## Estrutura

```
{{ cookiecutter.project_slug }}/
├── apps/                     # apps do projeto
{%- if cookiecutter.use_authentication == "yes" %}
│   └── accounts/             # autenticação por sessão
│       ├── models/ views/ forms/ services/ selectors/
│       ├── templates/        # registration/ e accounts/
│       ├── tests/
│       └── urls.py
{%- endif %}
├── core/
│   ├── settings/             # base / development / production
│   ├── management/commands/  # createapp, createseeder, seeder, reset_db, new_key
│   ├── templates/            # base, home, 404 (arquivos globais)
│   └── urls.py
├── seeders/                  # dados iniciais por app
├── static/                   # CSS{% if cookiecutter.use_htmx == "yes" %} e JS (HTMX){% endif %} + favicon
├── scripts/                  # start.sh{% if cookiecutter.use_docker == "yes" %}, entrypoint.sh{% endif %}
└── manage.py
```

Cada app segue uma estrutura base com **responsabilidades separadas em pacotes**:
`models/`, `views/`, `forms/`, `services/`, `selectors/`, `tests/` e `templates/<app>/`.

## Criar um app

```bash
sh django.sh createapp catalog product
```

Isso gera `models/`, `forms/`, `views/` (List/Create/Update/Delete), `services/`,
`selectors/`, `tests/`, `urls` e templates em `apps/catalog/`. Depois registre o app em
`core/settings/base.py` e inclua as rotas em
`core/urls.py` (o comando imprime as instruções).

## Seeders

```bash
sh django.sh createseeder catalog.product   # gera JSON de exemplo
sh django.sh seeder catalog                 # aplica (idempotente)
sh django.sh seeder --all                   # aplica todos
```

Antes do primeiro uso, gere a migração do app `core` (tabela de controle de seeders):

```bash
sh django.sh makemigrations core
sh django.sh migrate
```

{% if cookiecutter.use_tests == "yes" -%}
## Testes

```bash
make test
```

{% endif -%}
{% if cookiecutter.use_docker == "yes" -%}
## Docker

```bash
docker compose up --build
```

O banco{% if cookiecutter.database == "sqlite3" %} (SQLite em volume){% else %} ({{ cookiecutter.database }}){% endif %}
sobe junto e as migrations rodam no entrypoint.

{% endif -%}
## Deploy (checklist)

- `DJANGO_ENV=production`
- `DJANGO_SECRET_KEY` forte e secreta
- `DJANGO_ALLOWED_HOSTS` com o domínio real{% if cookiecutter.database != "sqlite3" %}, credenciais `DB_*`{% endif %}
- HTTPS na frente (o app usa `SECURE_PROXY_SSL_HEADER` + `SECURE_SSL_REDIRECT`)
- `collectstatic` executado (`scripts/start.sh` já faz)
- Superusuário via `DJANGO_SUPERUSER_*`

## Licença

{{ cookiecutter.license }}.
