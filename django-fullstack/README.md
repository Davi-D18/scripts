# Cookiecutter Django Full Stack

Template [cookiecutter](https://cookiecutter.readthedocs.io/) para gerar projetos Django
**full stack**: Django Template Language, Tailwind CSS, HTMX, autenticação por sessão,
settings por ambiente, seeders, pytest, Ruff, Docker e docker-compose.

> Este é o template **full stack**. Para APIs (DRF/JWT/Swagger), use o template `django-api`.

Construído seguindo o guia em `django-api/django-config-template.md`.

---

## Requisitos

- Python 3.12+
- Cookiecutter 2.6+: `pipx install cookiecutter`
- Node.js 20+ (apenas se `use_tailwind=yes`)
- Docker + Docker Compose (apenas se `use_docker=yes`)

## Uso

```bash
cookiecutter /home/ld/scripts/django-fullstack
```

Modo não interativo:

```bash
cookiecutter /home/ld/scripts/django-fullstack --no-input \
  project_name="Minha Loja" \
  database=postgresql use_authentication=yes use_docker=yes use_tailwind=yes use_htmx=yes
```

## Opções

| Opção | Valores | Descrição |
|-------|---------|-----------|
| `project_name` | texto | Nome legível do projeto |
| `project_slug` | texto | Nome do diretório/identificador (derivado) |
| `description` | texto | Descrição curta |
| `author_name` / `author_email` | texto | Autoria |
| `domain_name` | texto | Domínio de produção |
| `version` | texto | Versão inicial |
| `timezone` | texto | Ex.: `America/Sao_Paulo` |
| `language_code` | texto | Ex.: `pt-br` |
| `use_authentication` | `yes` / `no` | App de auth por sessão + templates |
| `database` | `postgresql` / `mysql` / `sqlite3` | Engine de **produção** (dev usa sqlite) |
| `dependency_manager` | `poetry` / `pip` | Gerenciador de dependências |
| `use_docker` | `yes` / `no` | `Dockerfile`, `docker-compose.yml`, entrypoint |
| `use_tailwind` | `yes` / `no` | Pipeline Tailwind (`package.json`, `input.css`) |
| `use_htmx` | `yes` / `no` | `static/js/htmx.min.js` + script no `base.html` |
| `use_tests` | `yes` / `no` | `pytest.ini`, `pytest-django` e testes |
| `license` | `MIT` / `BSD-3-Clause` / `GPL-3.0` / `Proprietary` | Gera `LICENSE` |

## O que é gerado

```
{{ project_slug }}/
├── apps/accounts/            # auth por sessão (se use_authentication=yes)
│                             #   models/ views/ forms/ services/ selectors/ tests/ templates/
├── core/
│   ├── management/commands/  # createapp (web), createseeder, seeder, reset_db, new_key
│   ├── settings/             # base / development / production + loader por DJANGO_ENV
│   ├── templates/            # base, home, 404 (globais)
│   ├── models.py             # SeederExecution
│   └── urls.py
├── seeders/
├── static/                   # css (Tailwind) + js (HTMX) + favicon.ico
├── Dockerfile / docker-compose.yml / .dockerignore   # se use_docker=yes
├── package.json / tailwind.config.js                 # se use_tailwind=yes
├── pytest.ini                                         # se use_tests=yes
├── Makefile, django.sh, pyproject.toml (Ruff), .pre-commit-config.yaml
└── scripts/entrypoint.sh, start.sh
```

Cada app usa uma estrutura base com responsabilidades separadas em pacotes
(`models/`, `views/`, `forms/`, `services/`, `selectors/`, `tests/`, `templates/<app>/`).
O comando `createapp` gera todos eles.

## Depois de gerar

```bash
cd <project_slug>
cp .env.example .env        # ajuste DJANGO_SECRET_KEY
make install                # poetry install  (ou pip install -r requirements-dev.txt)
make migrate
make tailwind               # compila o CSS (se use_tailwind=yes)
make run
```

Docker:

```bash
docker compose up --build
```

## Detalhes de implementação

- `core/templates/*` e `static/*` estão em `_copy_without_render` para não serem interpretados
  pelo Jinja (evita conflito com a sintaxe do Django Template Language).
- Arquivos condicionais (Docker, Tailwind, HTMX, auth, testes) são removidos no
  `hooks/post_gen_project.py`; o bloco de autenticação em `core/templates/base.html` é delimitado
  por `<!-- auth:start -->` / `<!-- auth:end -->`.
- `hooks/pre_gen_project.py` valida o `project_slug`.
- A migração inicial do app `core` (SeederExecution) é manual: rode `make makemigrations` /
  `python manage.py makemigrations core` na primeira vez antes de usar seeders.
- O CSS é "tailwind-agnóstico": `core/templates/base.html` usa classes semânticas (`.btn`, `.card`,
  `.container`) definidas tanto em `static/src/input.css` (Tailwind `@layer components`) quanto
  no fallback `static/css/main.css`. Assim funciona com ou sem `use_tailwind`.

## Manutenção do template

- Ao adicionar arquivos com sintaxe Django, inclua-os em `_copy_without_render`.
- Valide sempre a geração (ver abaixo).

```bash
# smoke test
cookiecutter . --no-input -o /tmp/gen \
  use_authentication=no database=sqlite3 use_docker=no use_tailwind=no use_tests=no
cd /tmp/gen/my_django_project
python -m venv .venv && .venv/bin/pip install -r requirements.txt
printf 'DJANGO_ENV=development\nDJANGO_SECRET_KEY=x\n' > .env
.venv/bin/python manage.py check
DJANGO_ENV=production .venv/bin/python manage.py check
```
