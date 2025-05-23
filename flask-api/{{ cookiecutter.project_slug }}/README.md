# {{ cookiecutter.project_name }}

Este template fornece uma estrutura inicial para aplicações Flask com suporte a:

- Organização por módulos (models, routes, services, repositories, schemas).
- Comandos CLI personalizados (`flask dev` e `flask db`).
- Migrações de banco com Flask-Migrate.
- Logging configurável com RotatingFileHandler.
- Tratamento padronizado de erros e respostas de sucesso.
- (Opcional) Middlewares de request/response.
- (Opcional) Documentação interativa via Swagger.

---

## Pré-requisitos

- Python 3.10+
- Cookiecutter instalado:
  ```bash
  pip install cookiecutter
  ```
- Dependências definidas em `requirements.txt` (serão instaladas após gerar o projeto).

## Gerando o Projeto

1. Execute o Cookiecutter apontando para este template:
   ```bash
   cookiecutter scripts/flask-template-v4
   ```
2. Responda ao prompt **project_name**: Nome do projeto (ex: `MeuProjeto`).  
   O `project_slug` será gerado automaticamente a partir do nome.

   Para as demais opções, selecione o número correspondente e pressione Enter:

   **usar_middlewares**:
   1) n (não) # Padrão
   2) s (sim)

   **usar_docs_api**:
   1) n (não) # Padrão
   2) s (sim)

   **banco_de_dados**:
   1) sqlite # Padrão
   2) mysql
   3) postgresql

3. Acesse a pasta criada:
   ```bash
   cd {{ cookiecutter.project_slug }}
   ```

4. Use o comando:
```bash
flask dev scaffold <nome dos arquivos>
```

5. Faça os ajustes nos arquivos gerados conforme necessário

6. Importe o arquivo de rotas gerado para o arquivo `__init__.py`:
```py
from .routes.arquivo import arquivo_bp
```

7. Registre as rotas dentro da função `create_app`:
```py
app.register_blueprint(variavel_bp)
```

8. Execute o comando de migração para criar a pasta `migrations`:
```bash
flask db init
```

9. Execute o comando para criar a primeira migrate:
```bash
flask db migrate -m "Nome da migrate"
```

10. Aplique as migrações no banco de dados:
```bash
flask db upgrade
```

11. Rode a aplicação com o comando:
```bash
flask dev run
```

## Configuração de Ambiente

Renomeie (ou copie) o arquivo de exemplo `.env` e ajuste variáveis:

```ini
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=True
PROPAGATE_EXCEPTIONS=True
{%- if cookiecutter.usar_docs_api == "s" %}
ENABLE_SWAGGER=True
{%- endif %}

# Configuração do banco de dados
{%- if cookiecutter.banco_de_dados == 'mysql' %}
DATABASE_URL=mysql://user:password@host:port/database
{%- elif cookiecutter.banco_de_dados == 'postgresql' %}
DATABASE_URL=postgresql://user:password@host:port/database
{%- else %}
# SQLite (padrão): não precisa alterar
{%- endif %}

LOG_LEVEL=DEBUG
LOG_MAX_BYTES=10000
LOG_BACKUP_COUNT=3
LOG_FILE=errors.log
```

> **Dica:** Caso use caracteres especiais na senha, faça URL-encode (ex: `@` → `%40`).

## Estrutura do Projeto

```
.
├── app
│   ├── commands       # Comandos CLI (db_commands, dev_commands)
│   ├── config         # Configurações de ambientes
│   ├── database       # Arquivo de banco SQLite (se usado) e configurações
│   ├── extensions     # Inicialização de Extensões
│   ├── logs           # Configuração de logging
│   ├── messages       # Erros e sucessos padronizados
│   ├── middlewares    # Middlewares HTTP (opcional)
│   ├── models         # Modelos ORM (SQLAlchemy)
│   ├── repositories   # Acesso a dados (gerado via scaffold)
│   ├── routes         # Blueprints e endpoints
│   ├── schemas        # Validação e serialização (Marshmallow)
│   └── services       # Lógica de negócio (gerado via scaffold)
├── migrations         # Migrações de banco (Flask-Migrate)
├── run.py             # Ponto de entrada da aplicação
├── requirements.txt   # Dependências do projeto
├── README.md          # Documentação (você está aqui)
└── swagger            # Esquemas OpenAPI YAML (opcional)
```

Cada módulo possui responsabilidade única:

- **models**: Definição das tabelas e campos.
- **repositories**: Funções CRUD diretas ao banco.
- **services**: Regras de negócio e tratamento de erros.
- **schemas**: Regras de validação e serialização.
- **routes**: Definição de endpoints e blueprints.

## Comandos Disponíveis

### Desenvolvimento (`flask dev`)

```bash
# Inicia servidor de desenvolvimento (com reload)
flask dev run --port 5000

# Executa linter (flake8)
flask dev lint

# Formata código (black)
flask dev format

# Abre shell interativo do Flask
flask dev shell

# Gera scaffold para recurso
flask dev scaffold <resource>
```

O comando `scaffold` criará automaticamente em `app/models`, `app/repositories`, `app/services`, `app/schemas` e `app/routes` um conjunto básico de arquivos.

### Banco de Dados (`flask db`)

```bash
# Inicializa pasta de migrações (apenas uma vez)
flask db init

# Gera nova migration com base nos modelos
flask db migrate -m "descrição"

# Aplica migrations pendentes
flask db upgrade

# Comandos extras:
flask db drop-all    # Remove todas as tabelas
flask db create-all  # Cria todas as tabelas
flask db reset       # Drop + Create
flask db backup      # Exporta backup (Postgres/MySQL/SQLite)
flask db restore     # Restaura backup
flask db shell       # Abre console DB (psql, mysql ou sqlite3)
```
{%- if cookiecutter.usar_middlewares == "s" %}
## Middlewares

As middlewares estão localizadas em `app/middlewares` 

Basta ajustar ou adicionar novos middlewares conforme necessário.
{%- endif %}

{%- if cookiecutter.usar_docs_api == "s" %}
## Documentação da API (Swagger)

o template inclui integração com **Flasgger**.

- Defina seus endpoints e na pasta `swagger/` ficam as informações sobre cada rota.
- Acesse `/docs/` para interface interativa.
{%- endif %}

Happy Coding! < LD /> :)