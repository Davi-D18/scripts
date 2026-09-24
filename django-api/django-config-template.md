# Template Django Full Stack com Cookiecutter — Guia de Construção

Documento de referência para construir e evoluir o template **Django Full Stack** usando a
biblioteca [cookiecutter](https://cookiecutter.readthedocs.io/). O foco é o template full stack
(Django Template Language + Tailwind CSS + HTMX), compartilhando uma base com o template de API.

> Este guia parte do template atual (`django-api`) já ajustado e mostra como reorganizá-lo em
> dois templates independentes — `cookiecutter-django-api` e `cookiecutter-django-fullstack` —
> ambos consumindo uma base comum (`cookiecutter-django-base`).

> **Status da implementação (atualizado):** os dois templates já existem como repositórios
> autocontidos em `django-api/` (somente API) e `django-fullstack/` (full stack). Delta em
> relação a este guia:
> - os templates **base** ficam em `core/templates/` (resolvidos via `APP_DIRS`, com
>   `core` em `INSTALLED_APPS`), e não em `templates/` na raiz;
> - o servidor de aplicação é o **Uvicorn** servindo **WSGI** por padrão
>   (`core.wsgi:application --interface wsgi`); para ASGI, troque para
>   `core.asgi:application`, em vez de Gunicorn;
> - a composição com `cookiecutter-django-base` (seção 4) ainda não foi feita; é o próximo
>   passo opcional.

---

## Sumário

1. [Objetivo e escopo](#1-objetivo-e-escopo)
2. [Conceitos do cookiecutter](#2-conceitos-do-cookiecutter)
3. [Arquitetura dos templates](#3-arquitetura-dos-templates)
4. [Base compartilhada](#4-base-compartilhada)
5. [Opções do cookiecutter](#5-opções-do-cookiecutter)
6. [Estrutura do projeto gerado](#6-estrutura-do-projeto-gerado)
7. [Configurações (settings)](#7-configurações-settings)
8. [Camada de aplicação](#8-camada-de-aplicação)
9. [Autenticação por sessão](#9-autenticação-por-sessão)
10. [Frontend: Tailwind + HTMX](#10-frontend-tailwind--htmx)
11. [Banco de dados e migrations](#11-banco-de-dados-e-migrations)
12. [Seeders](#12-seeders)
13. [Testes](#13-testes)
14. [Qualidade de código: Ruff + pre-commit](#14-qualidade-de-código-ruff--pre-commit)
15. [Docker](#15-docker)
16. [Makefile e scripts](#16-makefile-e-scripts)
17. [Hooks de geração](#17-hooks-de-geração)
18. [README e documentação gerada](#18-readme-e-documentação-gerada)
19. [Passo a passo de construção](#19-passo-a-passo-de-construção)
20. [Matriz de validação](#20-matriz-de-validação)
21. [Migração a partir do template atual](#21-migração-a-partir-do-template-atual)
22. [Convenções](#22-convenções)
23. [Decisões e trade-offs](#23-decisões-e-trade-offs)
24. [Apêndices](#24-apêndices)

---

## 1. Objetivo e escopo

### 1.1 Objetivo

Criar um template cookiecutter que gere, em segundos, um projeto Django **full stack** pronto
para desenvolvimento local e deploy em produção, com:

- Django 6.2 LTS (ou versão alvo definida), Python 3.12+.
- Django Template Language (DTL) server-side.
- Tailwind CSS com pipeline de build e HTMX para interatividade.
- Autenticação por **sessão** (sem DRF/JWT).
- Settings separados por ambiente (`base` / `development` / `production`).
- Seeders idempotentes, testes com pytest, lint/formatação com Ruff.
- Docker + docker-compose (app + banco), Ruff configurado, opções de geração em inglês.

### 1.2 Não-objetivo deste documento

- Não é o guia do template de API (DRF/JWT/Swagger). A base compartilhada é descrita, e o
  template de API é citado apenas como "irmão" que consome a mesma base.
- Não cobre CI/CD nem tipagem estática (mypy) — explicitamente fora do escopo por decisão.
- A migração inicial do app `core` permanece **manual** (`makemigrations core`).

### 1.3 Público-alvo

Desenvolvedores que vão manter o template. Assume familiaridade com Django, Jinja2 (base do
cookiecutter), Docker e npm básico.

---

## 2. Conceitos do cookiecutter

Entender estes 5 pontos evita 90% dos problemas.

### 2.1 `cookiecutter.json`

Arquivo na raiz do template que define as perguntas e os valores. Chaves com `_` (`_copy_without_render`,
`_extensions`, `_new_lines`) são configuração, não perguntas.

```json
{
  "project_name": "My Project",
  "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}",
  "use_authentication": ["yes", "no"]
}
```

### 2.2 Diretório `{{ cookiecutter.project_slug }}`

Todo o conteúdo que será copiado para o projeto gerado. O nome do diretório é ele mesmo um
template Jinja — por isso o slug vira o nome da pasta do projeto.

### 2.3 Hooks

Scripts em `hooks/` executados em momentos específicos, com o **diretório do projeto como cwd**:

| Hook | Quando roda | Uso típico |
|------|-------------|------------|
| `pre_prompt.py` | antes das perguntas | validar ambiente |
| `pre_gen_project.py` | após criar a pasta do projeto, antes de gerar arquivos | compor a base, validar variáveis |
| `post_gen_project.py` | após gerar todos os arquivos | remover arquivos condicionais, formatar, `git init` |

Detalhe importante verificado no cookiecutter 2.6:

- O `pre_gen_project` roda **depois** de a pasta do projeto existir e **antes** de os arquivos
  do template serem escritos.
- `generate_file` **sobrescreve** arquivos existentes por padrão (`skip_if_file_exists=False`).

Isso permite a composição descrita em [seção 4](#4-base-compartilhada): gerar a base no
`pre_gen` e deixar o template específico sobrescrever por cima.

### 2.4 `_copy_without_render`

Lista de padrões (fnmatch) cujo conteúdo **não** é renderizado pelo Jinja, apenas copiado.
No cookiecutter, `*` também casa com `/`, então `templates/*` cobre subpastas.

```json
"_copy_without_render": [
  "templates/*",
  "static/*",
  "core/management/commands/*.py"
]
```

### 2.5 Conflito Jinja x Django Template Language (DTL)

Esse é o erro clássico. Os dois usam `{{ }}` e `{% %}`, então um `.html` com DTL seria
destruído pelo Jinja do cookiecutter. **Solução obrigatória:** incluir `templates/*` em
`_copy_without_render`. Vale o mesmo para qualquer arquivo com sintaxe que colida (ex.: alguns
`.md`, JSON com chaves, scripts shell com `${...}` — estes últimos não colidem, mas avalie).

---

## 3. Arquitetura dos templates

### 3.1 Repositórios

```
scripts/
├── cookiecutter-django-base/         # base compartilhada (não é template standalone)
│   ├── {{ cookiecutter.project_slug }}/
│   │   └── core/ ...                  # plumbing comum
│   ├── hooks/
│   └── cookiecutter.json              # variáveis comuns (usadas via composição)
│
├── cookiecutter-django-api/          # template somente API (irmão)
│   └── ...
│
├── cookiecutter-django-fullstack/    # template full stack (foco deste guia)
│   ├── cookiecutter.json
│   ├── hooks/
│   │   ├── pre_gen_project.py         # compõe a base
│   │   └── post_gen_project.py        # ajustes finais
│   ├── _base/                         # git subtree da base (opcional, ver 4.2)
│   └── {{ cookiecutter.project_slug }}/
│       ├── apps/
│       ├── core/settings/             # settings específicos
│       ├── templates/
│       ├── static/
│       ├── Dockerfile
│       └── ...
│
└── django-api/                        # template atual (origem da evolução)
```

### 3.2 Por que separar API e Full Stack

- **Dependências limpas**: full stack não instala DRF/JWT/Swagger; API não instala npm/Tailwind.
- **Código sem condicionais**: o template único acumulava `{% if tipo_projeto %}` em settings,
  requirements e hooks. Separando (já feito), cada template é linear e legível.
- **Evolução independente**: mudar o pipeline de frontend não arranha o template de API.
- **Onboarding**: quem quer API não vê templates HTML; quem quer full stack não vê serializers.

### 3.3 Responsabilidade de cada repositório

| Camada | Repositório | Contém |
|--------|-------------|--------|
| Comum | `cookiecutter-django-base` | estrutura de pastas, loader de settings, seeders, comandos genéricos, `django.sh`, Ruff/pre-commit, pytest, Docker (base), Makefile (genérico), `.env.example`, README esqueleto, `.gitignore` |
| API | `cookiecutter-django-api` | deps DRF/JWT/Swagger, `core/configs/api`, `drf/swagger/jwt/cors`, app auth JWT, `createapp` REST, docs |
| Full Stack | `cookiecutter-django-fullstack` | deps Django/whitenoise, `templates/`, `static/`, Tailwind, HTMX, app auth por sessão, `createapp` web, Docker (frontend build), Makefile (tailwind) |

---

## 4. Base compartilhada

### 4.1 Princípio

A base fornece o "esqueleto comum". Os templates específicos **sobrescrevem** o que for
diferente. Isso mantém DRY sem acoplar demais.

### 4.2 Mecanismo recomendado: subtree + composição no `pre_gen`

1. A base é um repositório próprio (`cookiecutter-django-base`).
2. Cada template específico a incorpora em `_base/` via **git subtree** (vendorizada, offline,
   versionada):

   ```bash
   git subtree add --prefix=_base https://github.com/org/cookiecutter-django-base.git main --squash
   # atualizar depois:
   git subtree pull --prefix=_base https://github.com/org/cookiecutter-django-base.git main --squash
   ```

3. No `hooks/pre_gen_project.py`, o template roda o cookiecutter da base dentro do diretório do
   projeto (`overwrite_if_exists=True`), repassando o contexto. Em seguida, o cookiecutter gera
   os arquivos do template específico **por cima**, vencendo em caso de conflito.

   ```python
   # hooks/pre_gen_project.py (esboço)
   import os
   from cookiecutter.main import cookiecutter

   base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "_base")
   cookiecutter(
       template=base,
       no_input=True,
       output_dir=os.path.dirname(os.getcwd()),
       overwrite_if_exists=True,
       extra_context={
           "project_name": "{{ cookiecutter.project_name }}",
           "project_slug": "{{ cookiecutter.project_slug }}",
           "use_authentication": "{{ cookiecutter.use_authentication }}",
           "database": "{{ cookiecutter.database }}",
           "use_docker": "{{ cookiecutter.use_docker }}",
           "use_tests": "{{ cookiecutter.use_tests }}",
           "dependency_manager": "{{ cookiecutter.dependency_manager }}",
       },
   )
   ```

### 4.3 Alternativas (e por que não)

| Alternativa | Prós | Contras |
|-------------|------|---------|
| git submodule da base | histórico separado | `.git` no meio do template; cookiecutter renderiza o submodule; remoção no post_gen |
| download da base no hook (`git clone`) | sem vendoring | exige rede na geração; lento e frágil |
| symlink para a base | simples no dev | não portável (Windows/distribuição) |
| repositório único com subpastas | zero composição | contraria a decisão de repos separados |

### 4.4 Regras de precedência

Defina explicitamente: **template específico > base**. Se um arquivo da base precisar vencer,
não o duplique no específico. Documente isso no README do template.

---

## 5. Opções do cookiecutter

Todas em inglês, conforme decisão. Use `__prompts__` para textos de ajuda, mantendo as chaves
técnicas em inglês.

### 5.1 `cookiecutter.json` proposto

```json
{
  "project_name": "My Django Project",
  "project_slug": "{{ cookiecutter.project_name.lower().strip().replace(' ', '_').replace('-', '_') }}",
  "description": "A Django full stack project.",
  "author_name": "Your Name",
  "author_email": "you@example.com",
  "domain_name": "example.com",
  "version": "0.1.0",
  "timezone": "UTC",
  "language_code": "en-us",
  "use_authentication": ["yes", "no"],
  "database": ["postgresql", "mysql", "sqlite3"],
  "dependency_manager": ["poetry", "pip"],
  "use_docker": ["yes", "no"],
  "use_tailwind": ["yes", "no"],
  "use_htmx": ["yes", "no"],
  "use_tests": ["yes", "no"],
  "license": ["MIT", "BSD-3-Clause", "GPL-3.0", "Proprietary"],
  "_copy_without_render": [
    "templates/*",
    "static/*",
    "core/management/commands/*.py"
  ],
  "__prompts__": {
    "project_name": "Project name",
    "project_slug": "Project slug (directory name)",
    "description": "Short project description",
    "author_name": "Author name",
    "author_email": "Author email",
    "domain_name": "Domain name",
    "version": "Initial version",
    "timezone": "Timezone (e.g. America/Sao_Paulo)",
    "language_code": "Language code (e.g. pt-br)",
    "use_authentication": "Include session authentication?",
    "database": "Database engine",
    "dependency_manager": "Dependency manager",
    "use_docker": "Include Docker and docker-compose?",
    "use_tailwind": "Include Tailwind CSS pipeline?",
    "use_htmx": "Include HTMX?",
    "use_tests": "Include pytest setup?",
    "license": "License"
  }
}
```

### 5.2 Regras de escolha

- Defaults na **primeira posição** de cada lista.
- `use_tailwind`/`use_htmx` só fazem sentido com `use_tailwind=yes` (valide no `pre_prompt`).
- `database=sqlite3` deve funcionar em produção (fallback para arquivo local) — evita o bug
  "produção quebra" encontrado no template atual.
- `dependency_manager` controla Makefile, README e pyproject/requirements.

### 5.3 Validação das respostas

No `hooks/pre_prompt.py` (ou `pre_gen_project.py`) valide slugs e combinações inválidas:

```python
import re
slug = "{{ cookiecutter.project_slug }}"
if not re.fullmatch(r"[a-z][a-z0-9_]*", slug):
    raise SystemExit(f"Invalid project_slug: {slug}. Use lowercase, digits and underscore.")
```

---

## 6. Estrutura do projeto gerado

```
my_project/
├── apps/
│   ├── __init__.py
│   └── accounts/                    # app de exemplo (auth por sessão)
│       ├── migrations/
│       ├── templates/accounts/
│       ├── tests/
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       └── views.py
├── core/
│   ├── configs/                     # opcional: CORS etc. (full stack normalmente não usa)
│   ├── management/commands/         # createapp web, createseeder, seeder, reset_db, new_key
│   ├── settings/
│   │   ├── __init__.py              # loader por DJANGO_ENV
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── templates/                   # templates globais (base.html, 404.html)
│   ├── utils/
│   ├── admin.py
│   ├── models.py                    # SeederExecution
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── seeders/
├── static/
│   ├── css/                         # main.css (gerado) 
│   ├── js/                          # htmx.min.js (vendorizado)
│   └── src/input.css                # fonte Tailwind
├── templates/
│   ├── base.html
│   ├── home.html
│   └── registration/
│       ├── login.html
│       ├── register.html
│       └── logged_out.html
├── scripts/
│   ├── start.sh
│   └── entrypoint.sh                # Docker
├── .dockerignore
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
├── django.sh
├── Makefile
├── manage.py
├── package.json
├── pyproject.toml                   # Poetry + Ruff
├── ruff.toml (ou [tool.ruff])       # ver apêndice
├── pytest.ini
├── tailwind.config.js
└── README.md
```

`templates/` na raiz (global) + `apps/<app>/templates/<app>/` (namespace por app) é a
organização recomendada: `APP_DIRS=True` + `DIRS=[BASE_DIR / "templates"]`.

---

## 7. Configurações (settings)

### 7.1 Estratégia

Repetir o padrão atual (classe base + subclasses por ambiente), que é um bom acerto:

```python
# core/settings/__init__.py
import sys
from importlib import import_module
from decouple import config

DJANGO_ENV = config("DJANGO_ENV", "development")
SETTINGS_MODULES = {
    "development": "core.settings.development.DevelopmentSettings",
    "production": "core.settings.production.ProductionSettings",
}
module_path, class_name = SETTINGS_MODULES[DJANGO_ENV].rsplit(".", 1)
Settings = getattr(import_module(module_path), class_name)
_instance = Settings()
for _attr in dir(_instance):
    if _attr.isupper():
        setattr(sys.modules[__name__], _attr, getattr(_instance, _attr))
```

`core/settings/base.py` define tudo o que é comum:

- `BASE_DIR`, `SECRET_KEY` (via `decouple`), `INSTALLED_APPS`, `MIDDLEWARE`, `TEMPLATES`,
  `DATABASES` (dev sqlite + prod com o engine escolhido), `STATIC_*`, `MEDIA_*`, `LANGUAGE_CODE`,
  `TIME_ZONE`, `DEFAULT_AUTO_FIELD`, `AUTH_PASSWORD_VALIDATORS`, `EMAIL_*`.
- Métodos `select_database()` e `print_environment_info()`.

### 7.2 Dados específicos do full stack

```python
# em BaseSettings
STATICFILES_DIRS = [BASE_DIR / "static"]

# autenticação por sessão
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
```

### 7.3 Variáveis de ambiente (`.env.example`)

```
DJANGO_ENV=development
DJANGO_SECRET_KEY=change-me
DJANGO_ALLOWED_HOSTS=
DJANGO_CORS_ALLOWED_ORIGINS=      # somente se houver integração externa
DB_NAME=app
DB_USER=app
DB_PASSWORD=app
DB_HOST=localhost
DB_PORT=5432
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_PASSWORD=
```

### 7.4 Segurança de produção (não esquecer)

```python
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # essencial atrás de proxy
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "DENY"
```

E `ALLOWED_HOSTS` lido direto do env no full stack (sem CORS config para não introduzir
dependência desnecessária).

---

## 8. Camada de aplicação

### 8.1 Organização de apps

- Apps ficam em `apps/<app>` com `AppConfig.name = "apps.<app>"`.
- Registrar sempre como `apps.<app>` em `INSTALLED_APPS`.
- Comando `createapp` próprio (adaptado para web) cria o scaffold.

### 8.2 Camadas internas de um app

Para full stack, cada app separa as responsabilidades em pacotes:

```
apps/<app>/
├── models/          # dados (um módulo por modelo + __init__ exportando)
├── selectors/       # leitura (queries)
├── services/        # escrita / regras de negócio
├── forms/           # validação de entrada
├── views/           # orquestração HTTP (uma view por módulo)
├── urls.py
├── admin.py
├── templates/<app>/
└── tests/
```

- **views** finas: recebem request, chamam selector/service, renderizam template.
- **services** concentram regras de negócio (fáceis de testar sem HTTP).
- **selectors** encapsulam queries reutilizáveis.
- Evita lógica de negócio em views e templates.

### 8.3 `createapp` web

Evolua o comando atual (que gera `controllers/schemas/routes` de DRF) para um scaffold web
com estrutura em pacotes:

```
apps/<app>/
├── views/<resource>.py
├── forms/<resource>.py
├── models/<resource>.py
├── services/            # regras de negócio (opcional)
├── selectors/           # consultas (opcional)
├── urls.py
├── templates/<app>/<resource>_list.html
├── templates/<app>/<resource>_form.html
└── tests/
```

Regras importantes já aprendidas:

- Usar o **app label** (`apps.<app>`) em imports/routes, não o nome do recurso.
- Gerar modelo sem `ordering=['name']`/`self.name` inexistentes (quebra `manage.py check`).
- Exportar o modelo em `models/__init__.py` (seeders importam `from apps.<app>.models import X`).
- Tratar `AppConfig.name` com aspas simples ou duplas (o `startapp` gera com aspas simples).

### 8.4 `core/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("", include("apps.accounts.urls")),
]
```

---

## 9. Autenticação por sessão

Sem DRF/JWT. Use o que o Django oferece.

### 9.1 Views

Em `apps/accounts/urls.py`:

```python
from django.contrib.auth import views as auth_views
from django.urls import path
from apps.accounts.views import RegisterView

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
```

`views.py`:

```python
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.accounts.forms import UserRegisterForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
```

`forms.py`:

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")
```

### 9.2 Pontos de atenção

- Em Django 5, `LogoutView` exige **POST** — o template de logout deve usar `<form method="post">`.
- Templates em `templates/registration/` (`login.html`, `register.html`, `logged_out.html`).
- `AUTH_PASSWORD_VALIDATORS` definido no base (o template atual não tinha).
- Áreas protegidas com `LoginRequiredMixin` / `@login_required`.

---

## 10. Frontend: Tailwind + HTMX

### 10.1 Pipeline do Tailwind

Escolha uma das abordagens; a recomendada é **npm + Tailwind CLI** (previsível e versionável).

```
package.json
tailwind.config.js
static/src/input.css     # @tailwind base/components/utilities + @layer components
static/css/main.css      # gerado (não editar)
```

`package.json`:

```json
{
  "name": "{{ cookiecutter.project_slug }}-frontend",
  "private": true,
  "scripts": {
    "build": "tailwindcss -i ./static/src/input.css -o ./static/css/main.css --minify",
    "watch": "tailwindcss -i ./static/src/input.css -o ./static/css/main.css --watch"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.17"
  }
}
```

`tailwind.config.js`:

```js
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
    "./apps/**/*.py",
  ],
  theme: { extend: {} },
  plugins: [],
};
```

Alternativas: `django-tailwind` (integra ao manage.py, mas adiciona dependência e fluxo próprio),
ou Tailwind standalone binary (sem Node, porém binário por plataforma).

### 10.2 HTMX

Vendorize `htmx.min.js` em `static/js/htmx.min.js` (melhor que CDN para produção/offline) e
inclua no `base.html`:

```html
<script src="{% static 'js/htmx.min.js' %}" defer></script>
```

Habilitar CSRF para HTMX (necessário em POST/AJAX):

```html
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```

### 10.3 Templates base e componentes

- `templates/base.html`: `<head>` com CSS/HTMX, navegação, blocos `{% block content %}`.
- Componentizar com `{% include %}` (ex.: `components/button.html`, `components/nav.html`).
- `templates/registration/*` para auth.
- `templates/<app>/*` para telas de cada app.

Exemplo de bloco de auth no `base.html` (importante: marcar para remoção condicional):

```html
<!-- auth:start -->
<div class="flex items-center gap-4">
  {% if user.is_authenticated %}
    <span>Olá, {{ user.username }}</span>
    <form method="post" action="{% url 'logout' %}">{% csrf_token %}
      <button class="btn" type="submit">Sair</button>
    </form>
  {% else %}
    <a class="btn" href="{% url 'login' %}">Entrar</a>
  {% endif %}
</div>
<!-- auth:end -->
```

O `post_gen_project.py` remove o bloco `auth:start`–`auth:end` quando `use_authentication=no`,
evitando `NoReverseMatch` de rotas de auth inexistentes.

### 10.4 Static files

- `STATICFILES_DIRS = [BASE_DIR / "static"]`, `STATIC_ROOT = BASE_DIR / "staticfiles"`.
- WhiteNoise para servir estáticos em produção (já no projeto atual).
- Considere `CompressedManifestStaticFilesStorage` para cache-busting e compressão.

---

## 11. Banco de dados e migrations

- **Dev**: SQLite sempre (`database.db`), independentemente da escolha.
- **Prod**: engine escolhida (`postgresql`/`mysql`/`sqlite3`), credenciais via env.
- Garantir que `database=sqlite3` **também** funcione em produção (definir entrada
  `production` com engine sqlite e arquivo próprio, ex.: `production.db`).
- Migrations: o app `core` (SeederExecution) exige `makemigrations core` (decisão: manter
  manual). Documentar no README.
- Para produção, `migrate` no entrypoint/`start.sh`.

---

## 12. Seeders

Reaproveitar o sistema atual, que é bom:

- `createseeder app.Model` gera `seeders/<app>/<model>_seeder.py` + `seeders/<app>/data/<Model>.json`.
- `seeder <app>` / `seeder --all` / `--check` / `--force`, com hash do JSON para idempotência
  (modelo `core.SeederExecution`).
- Importar modelos via `from apps.<app>.models import <Model>` — por isso o `createapp` deve
  exportar em `models/__init__.py`.

---

## 13. Testes

### 13.1 Dependências

```
pytest
pytest-django
pytest-cov
```

### 13.2 `pytest.ini`

```ini
[pytest]
DJANGO_SETTINGS_MODULE = core.settings.development
python_files = tests.py test_*.py *_tests.py
addopts = -q
```

### 13.3 Estrutura

- `apps/<app>/tests/test_views.py`, `test_services.py`, `test_forms.py`, `test_models.py`.
- `conftest.py` com fixtures comuns (cliente, usuário, factories).
- Cobrir: render das telas principais, fluxo de login/registro/logout, services.
- Smoke test de templates pegando erros de `{% url %}`/sintaxe.

---

## 14. Qualidade de código: Ruff + pre-commit

Substituir black + isort + flake8 por **Ruff** (rápido, um só binário/config).

`pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"
exclude = ["migrations", ".venv", "venv", "staticfiles", "node_modules"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "DJ", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
```

`select` inclui `I` (isort), `B` (bugbear) e `DJ` (django). `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-added-large-files
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: local
    hooks:
      - id: django-check
        name: Django check
        entry: python manage.py check
        language: system
        pass_filenames: false
        types: [python]
```

---

## 15. Docker

### 15.1 Dockerfile multi-stage

Estágio Node compila o Tailwind; estágio Python instala deps e copia o CSS compilado.

```dockerfile
# ---------- frontend ----------
FROM node:20-alpine AS frontend
WORKDIR /app
COPY package.json ./
RUN npm install
COPY tailwind.config.js ./
COPY static/src ./static/src
COPY templates ./templates
COPY apps ./apps
RUN npm run build

# ---------- python ----------
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=frontend /app/static/css/main.css ./static/css/main.css

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["./scripts/entrypoint.sh"]
```

### 15.2 `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 5s
      retries: 5

  web:
    build: .
    command: ./scripts/entrypoint.sh
    env_file: .env
    environment:
      DJANGO_ENV: production
      DB_HOST: db
      DB_PORT: 5432
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

volumes:
  pgdata:
```

### 15.3 `scripts/entrypoint.sh`

```bash
#!/usr/bin/env sh
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec python -m uvicorn core.wsgi:application --interface wsgi --host 0.0.0.0 --port 8000
```

### 15.4 `.dockerignore`

```
.venv
venv
node_modules
__pycache__
*.pyc
.git
staticfiles
media
database.db
.env
```

---

## 16. Makefile e scripts

```makefile
.PHONY: install format lint test tailwind tailwind-watch migrate run docker-up

install:
	poetry install

format:
	ruff format .
	ruff check --fix .

lint:
	ruff check .

test:
	pytest

tailwind:
	npm install
	npm run build

tailwind-watch:
	npm run watch

migrate:
	python manage.py migrate

run:
	python manage.py runserver

docker-up:
	docker compose up --build
```

Condicione alvos conforme `dependency_manager`, `use_docker`, `use_tailwind`. `django.sh`
(compatibilidade Windows) permanece.

---

## 17. Hooks de geração

### 17.1 `pre_gen_project.py`

- Valida respostas e combinações.
- Roda o cookiecutter da base (`_base/`) com `overwrite_if_exists=True`.

### 17.2 `post_gen_project.py`

Responsabilidades:

1. Remover arquivos condicionais:
   - `use_authentication=no` → remover app de auth e o bloco `auth:start/end` dos templates.
   - `use_tailwind=no` → remover `package.json`, `tailwind.config.js`, `static/src`, alvos do Makefile.
   - `use_htmx=no` → remover `static/js/htmx.min.js` e o `<script>` no `base.html`.
   - `use_docker=no` → remover `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `entrypoint.sh`.
   - `use_tests=no` → remover `pytest.ini` e deps de teste.
2. Formatar/validar (ex.: `ruff format` se disponível).
3. `git init` opcional e mensagem final com próximos passos.

Exemplo de remoção de bloco condicional em arquivo não renderizado:

```python
from pathlib import Path

base = Path.cwd() / "templates" / "base.html"
content = base.read_text()
start, end = "<!-- auth:start -->", "<!-- auth:end -->"
if "{{ cookiecutter.use_authentication }}" == "no" and start in content:
    base.write_text(content.split(start)[0] + content.split(end, 1)[1])
```

### 17.3 Ordem importa

Sempre remova arquivos **depois** de gerar e **antes** de formatar/commitar. O `_copy_without_render`
não impede a remoção — ela é feita no filesystem gerado.

---

## 18. README e documentação gerada

O `README.md` do projeto gerado deve ser renderizado pelo Jinja e cobrir:

- Visão geral e stack.
- Pré-requisitos (Python, Node, Docker).
- Setup local: `.env`, `make install`, `make migrate`, `make tailwind`, `make run`.
- Setup via Docker: `docker compose up --build`.
- Comandos (`django.sh`, `make`).
- Estrutura de pastas.
- Como criar um app (`createapp`), models, templates.
- Seeders.
- Testes.
- Checklist de deploy (variáveis, `collectstatic`, proxy header, superuser).

Mantenha seções condicionais (`{% if use_tailwind %}` etc.) para não documentar o que não foi gerado.

---

## 19. Passo a passo de construção

### Passo 0 — Preparar workspace

```bash
mkdir -p scripts && cd scripts
# repositórios: cookiecutter-django-base, cookiecutter-django-api, cookiecutter-django-fullstack
```

### Passo 1 — Extrair a base (`cookiecutter-django-base`)

1. Copiar do template atual o que é comum: `core/` (loader de settings, utils, management
   commands genéricos), `seeders/` conventions, `django.sh`, `.gitignore`, Ruff/pre-commit,
   `pytest.ini`, `.env.example`, Docker base, Makefile genérico, README esqueleto.
2. Torná-lo um template cookiecutter com `cookiecutter.json` das variáveis comuns.
3. Publicar o repo.

### Passo 2 — Criar `cookiecutter-django-fullstack`

1. `git subtree add --prefix=_base <base> main --squash`.
2. Criar `cookiecutter.json` (seção 5).
3. Criar `hooks/pre_gen_project.py` que compõe a `_base`.
4. Criar o overlay: `core/settings/*`, `core/urls.py`, `templates/`, `static/`,
   `apps/accounts/`, `package.json`, `tailwind.config.js`, `Dockerfile`, `docker-compose.yml`,
   Makefile (tailwind), `createapp` web.
5. Ajustar `_copy_without_render` para `templates/*` e `static/*`.

### Passo 3 — Adaptar comandos

1. `createapp` → scaffold web (views/forms/templates).
2. `createseeder`/`seeder` → manter.
3. Remover `core/configs/api`, `formatters` de DRF.

### Passo 4 — Testar geração (ver seção 20)

### Passo 5 — Publicar e versionar

- Tags semver (`v1.0.0`).
- Documentar no README do template como atualizar a `_base`.

---

## 20. Matriz de validação

Sempre que alterar o template, gere e rode `manage.py check` nas combinações:

| Cenário | auth | db | docker | tailwind | tests | Esperado |
|---------|------|----|--------|----------|-------|----------|
| Mínimo | no | sqlite3 | no | no | no | `check` dev+prod OK |
| Padrão | yes | postgresql | yes | yes | yes | `check` + `docker build` OK |
| Sem frontend | yes | sqlite3 | no | no | yes | `check` OK; sem `package.json` |
| Sem auth | no | mysql | yes | yes | no | bloco auth removido; `check` OK |

Script de smoke (gera e checa):

```bash
cookiecutter ./cookiecutter-django-fullstack --no-input -o /tmp/gen \
  use_authentication=no database=sqlite3 use_docker=no use_tailwind=no use_tests=no
cd /tmp/gen/my_django_project
python -m venv .venv && .venv/bin/pip install -r requirements.txt
printf 'DJANGO_ENV=development\nDJANGO_SECRET_KEY=x\n' > .env
.venv/bin/python manage.py check
DJANGO_ENV=production .venv/bin/python manage.py check
```

Valide também:

- Render de templates via `django.test.Client` (`/`, `/login/`, `/register/`).
- `createapp` com recurso igual e diferente do app.
- `createseeder` + `seeder` (após `makemigrations core`).
- `ruff check` sem erros.
- `docker compose build`.

---

## 21. Migração a partir do template atual

O template `django-api` original tinha um switch `tipo_projeto`. A migração já foi executada
(`django-api` ficou API-only e `django-fullstack` foi criado). O roteiro seguido foi:

1. **Inventariar** os arquivos atuais e classificar em: comum, API, full stack.
2. **Criar a base** com os comuns (seção 4 / passo 1).
3. **Criar `cookiecutter-django-api`** movendo os arquivos de API + removendo os `{% if
   tipo_projeto %}` (linearização).
4. **Criar `cookiecutter-django-fullstack`** com os arquivos web + base composta.
5. **Correções já aplicadas no atual devem ser levadas**: DB de produção com sqlite, `createapp`
   com app label, `AppConfig` com aspas, modelo sem `ordering` inválido, `__init__` exportando
   modelo, CORS com env vazio, `SECURE_PROXY_SSL_HEADER`, `BrowsableAPIRenderer` só em dev
   (no API), `pytest-django`.
6. **Manter um `django-api/` legado** por um tempo, ou arquivar após validar os dois novos.

---

## 22. Convenções

- Opções do cookiecutter **em inglês**; textos de ajuda via `__prompts__`.
- `python_slug`: minúsculo, `[a-z0-9_]`.
- Imports absolutos (`apps.<app>...`).
- `AppConfig.name = "apps.<app>"`.
- Sem lógica de negócio em views/templates (usar services/selectors).
- Migrations nunca editadas à mão.
- `_copy_without_render` para tudo que tenha `{{`/`{%` que não seja Jinja do cookiecutter.
- Um único formato por projeto (Poetry ou pip, não ambos).

---

## 23. Decisões e trade-offs

| Decisão | Motivo | Trade-off |
|---------|--------|-----------|
| Dois repos + base por subtree | organização e deps limpas | sincronizar a base requer `git subtree pull` |
| Composição no `pre_gen` | reaproveita cookiecutter nativo, offline | hook um pouco mais complexo |
| Tailwind via npm | previsível, versionável | exige Node no build (resolvido no multi-stage) |
| Auth por sessão | simples, sem DRF | sem tokens para clientes externos (aí use o template API) |
| Ruff em vez de black/isort/flake8 | um só tool, rápido | pouca curva de migração |
| Core migration manual | decisão do projeto | passo a mais no setup |
| Sem CI/mypy | escopo | qualidade fica manual |

---

## 24. Apêndices

### Apêndice A — `cookiecutter.json` mínimo da base

```json
{
  "project_name": "My Project",
  "project_slug": "{{ cookiecutter.project_name.lower().strip().replace(' ', '_').replace('-', '_') }}",
  "database": ["postgresql", "mysql", "sqlite3"],
  "dependency_manager": ["poetry", "pip"],
  "use_docker": ["yes", "no"],
  "use_tests": ["yes", "no"]
}
```

### Apêndice B — `ruff.toml` alternativo

```toml
line-length = 88
target-version = "py312"

[lint]
select = ["E", "F", "I", "B", "DJ", "UP"]
ignore = ["E501"]

[format]
quote-style = "double"
```

### Apêndice C — `.gitignore` (trechos)

```
__pycache__/
*.py[cod]
.venv/
venv/
.env
database.db
production.db
media/
staticfiles/
node_modules/
static/css/main.css   # se preferir não versionar o compilado
```

### Apêndice D — Checklist final do template

- [ ] `cookiecutter.json` com defaults e `__prompts__`
- [ ] `templates/*` e `static/*` em `_copy_without_render`
- [ ] `pre_gen_project` compõe a base; `post_gen_project` remove condicionais
- [ ] Sem `{% if %}` residuais em arquivos que deveriam ser específicos
- [ ] `manage.py check` OK em dev e produção para todos os cenários
- [ ] Render de `/`, `/login/`, `/register/` sem erro de template
- [ ] Docker build OK com Tailwind compilado
- [ ] Ruff sem erros; pre-commit instalado
- [ ] README reflete as opções escolhidas
- [ ] Seeders funcionam após `makemigrations core`
- [ ] Tag de versão publicada

---

## Referências

- Cookiecutter: <https://cookiecutter.readthedocs.io/>
- Cookiecutter hooks: <https://cookiecutter.readthedocs.io/en/stable/advanced/hooks.html>
- Cookiecutter `_copy_without_render`: <https://cookiecutter.readthedocs.io/en/stable/advanced/templates.html>
- Django settings: <https://docs.djangoproject.com/en/stable/topics/settings/>
- Ruff: <https://docs.astral.sh/ruff/>
- Tailwind CSS: <https://tailwindcss.com/docs/installation>
- HTMX: <https://htmx.org/docs/>
