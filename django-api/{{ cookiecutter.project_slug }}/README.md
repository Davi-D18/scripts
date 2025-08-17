## 🚀 Configuração

### Ambiente de Produção
```bash
pip install -r requirements.txt
sh scripts/start.sh
```

### Ambiente de Desenvolvimento
```bash
sh django.sh migrate
```

## 🛠 Comandos de Desenvolvimento

### Formatação de Código
```bash
make format    # Formatar com black + isort
```

### Verificação de Qualidade
```bash
make lint      # Verificar com flake8 + mypy
```

### Testes
```bash
make test      # Executar testes com pytest
```

### Limpeza
```bash
make clean     # Remover arquivos temporários
```

## 📦 Dependências

- **requirements.txt**: Dependências de produção
- **requirements-dev.txt**: Dependências de desenvolvimento (inclui produção)

## 🔧 Ferramentas Configuradas

- **Black**: Formatação automática de código
- **isort**: Organização de imports
- **Flake8**: Linting e verificação de estilo
- **MyPy**: Type checking
- **Pytest**: Framework de testes



## 1. Configuração inicial

### 1.1 Renomear arquivo de ambiente
Após criar o projeto com cookiecutter, renomeie o arquivo de configuração:
```bash
mv .env.example .env
```

### 1.2 Configurar variáveis de ambiente
Edite o arquivo `.env` e configure as seguintes variáveis:

**Configurações obrigatórias:**
- `DJANGO_SECRET_KEY`: Gere uma nova chave usando `sh django.sh new_key`

**Apenas para Produção:**
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CORS_ALLOWED_ORIGINS`

**Configurações de banco de dados:**
{%- if cookiecutter.banco_de_dados == "sqlite3" %}
- Está configurado o SQLite3, não precisa configurar credenciais de banco, apenas o nome do arquivo que será gerado em `core/settings/base.py`
{%- else %}
- Você escolheu **{{ cookiecutter.banco_de_dados|upper }}**: preencha as credenciais do banco no arquivo `.env`:
  - `DB_NAME`: Nome do banco de dados
  - `DB_USER`: Usuário do banco
  - `DB_PASSWORD`: Senha do banco
  - `DB_HOST`: Host do banco (ex: localhost)
  - `DB_PORT`: Porta do banco ({{ "3306" if cookiecutter.banco_de_dados == "mysql" else "5432" }}) padrão
{%- endif %}

**Nota importante:** No desenvolvimento, sempre será usado SQLite3, independente da escolha. O banco configurado será usado apenas em produção, porém nada impede de alterar.

### 1.3 Gerar chave secreta
```bash
sh django.sh new_key
```
Copie a chave gerada e cole no arquivo `.env` na variável `DJANGO_SECRET_KEY`.

{%- if cookiecutter.use_authentication == "yes" %}
### Configurar autenticação JWT
Configure a chave JWT no arquivo `.env`:
```bash
sh django.sh new_key  # Use a mesma chave ou gere uma nova
```
Copie a chave gerada e cole na variável `JWT_SECRET_KEY` no arquivo `.env`.

**Endpoints de autenticação disponíveis:**
- `POST /api/v1/auth/login/` - Login (retorna access e refresh token)
- `POST /api/v1/auth/login/refresh/` - Renovar token
- `POST /api/v1/auth/register/` - Registrar
{%- endif %}

{%- if cookiecutter.use_documentation == "yes" %}
### Configurar documentação Swagger
Para configurar, basta ir em `core/configs/libs/swagger.py` e então configuar da forma que achar melhor. A instância da classe de configuração é automaticamente importada em `core/settings/base.py` usada tanto em produção como em desenvolvimento

**Documentação disponível em:**
- `/docs/` - Interface Swagger
{%- endif %}

## 2. Estrutura de configurações

O projeto possui 3 arquivos de configuração em `core/settings/`:
- `base.py`: Configurações base para desenvolvimento e produção
- `development.py`: Configurações específicas para desenvolvimento
- `production.py`: Configurações específicas para produção

## 3. Criando seu primeiro app

### 3.1 Criar estrutura do app
```bash
sh django.sh createapp nome_do_app
```

Isso criará a estrutura:
```
apps/nome_do_app/
├── controllers/
├── models/
├── schemas/
├── services/
├── routes/
├── migrations/
└── tests/
```

**Nota**: A estrutura pode ser modificada caso queira

### 3.2 Registrar o app
Em `core/settings/base.py`, adicione o app em `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'apps.nome_do_app',
]
```

### 3.3 Configurar models
Crie seus modelos de banco de dados no diretório `models` e importe eles dentro do `__init__.py` dessa forma:

```py
from .produtos import Produtos # Nome do model criado

__all__ = ["Produtos"]
```

### 3.4 Criar migrações e aplicar
```bash
sh django.sh makemigrations
sh django.sh makemigrations core  # Opcional: Necessário para criar migrações do sistema de controle de seeders
sh django.sh migrate
```

### 3.5 Configurar URLs
Em `core/urls.py`, registre as rotas do seu app:
```python
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.nome_do_app.urls')),
]
```

### 3.6 Executar servidor
```bash
sh django.sh runserver
```

## 4. Exemplo prático

### 4.1 Modelo (apps/produtos/models/produto.py)
```python
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
```

### 4.2 Schema (apps/produtos/schemas/produto_schema.py)
```python
from rest_framework import serializers
from apps.produtos.models.produto import Produto

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
```

### 4.3 Controller (apps/produtos/controllers/produto_controller.py)
```python
from rest_framework import viewsets
from apps.produtos.models.produto import Produto
from apps.produtos.schemas.produto_schema import ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
```

### 4.4 Rotas (apps/produtos/routes/)
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.produtos.controllers.produto_controller import ProdutoViewSet

router = DefaultRouter()
router.register('produtos', ProdutoViewSet)

urlpatterns = [
    path('', include(router.urls))
]
```

## 5. Sistema de Seeders (Opcional)

Para popular o banco de dados com dados iniciais:

### 5.1 Criar seeder
```bash
sh django.sh createseeder nome_do_app.nome_do_model
# Exemplo: sh django.sh createseeder produtos.produto
# produtos: Nome do app que deseja criar um seeder
# produto: nome do model dentro do app 'produtos'
```

### 5.2 Configurar dados
Edite o arquivo JSON gerado em `seeders/nome_do_app/data/nome_do_model.json` com os dados desejados.

### 5.3 Aplicar seeders
```bash
sh django.sh seeder nome_do_app
```

**Parâmetros disponíveis para o comando seeder:**
- `sh django.sh seeder app_name` - Executa todos os seeders do app
- `sh django.sh seeder app_name seeder_name` - Executa seeder específico
- `sh django.sh seeder --all` - Executa todos os seeders do projeto
- `sh django.sh seeder --check` - Verifica status sem executar
- `sh django.sh seeder --force` - Força execução mesmo se já aplicado

## 6. Comandos disponíveis

Todos os comandos devem ser executados com `sh django.sh` para garantir compatibilidade com Windows:

- `sh django.sh runserver` - Inicia o servidor
- `sh django.sh makemigrations` - Cria migrações
- `sh django.sh migrate` - Aplica migrações
- `sh django.sh createapp nome_app` - Cria novo app
- `sh django.sh createseeder app.model` - Cria seeder
- `sh django.sh seeder app_name` - Executa seeders
- `sh django.sh new_key` - Gera nova chave secreta
- `sh django.sh createsuperuser` - Cria superusuário
- `sh django.sh shell` - Abre shell do Django
- `sh django.sh collectstatic` - Coleta arquivos estáticos

### Ver lista de comandos disponíveis:
```bash
sh django.sh help
```

### Ver detalhes de um comando:
```bash
sh django.sh help NOME_DO_COMANDO
```

## 7. Estrutura do projeto

```
project_name/
├── apps/                    # Seus apps
├── core/                    # Configurações do projeto
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── management/commands/ # Comandos personalizados
│   ├── urls.py
│   └── configs/libs         # Configurações de libs
├── scripts/                 # Scripts de automação
│   └── start.sh            # Script de inicialização para produção
├── seeders/                 # Seeders organizados por app
├── django.sh               # Script para comandos
├── .env.example            # Exemplo de configuração
└── manage.py
```

## 8. Dicas importantes

- **Windows**: Sempre use `sh django.sh` em vez de `python manage.py`
- **Banco de dados**: SQLite3 é usado no desenvolvimento, independente da escolha, porém pode ser alterado caso queira
- **Configurações**: Edite `core/settings/base.py` para configurações gerais
- **Apps**: Sempre registre novos apps em `INSTALLED_APPS` usando o formato `apps.nome_app`
- **Migrações**: Execute `makemigrations core` após `makemigrations` para incluir migrações do sistema de seeders

## 9. Próximos passos

1. Configure seu `.env`
2. Crie seu primeiro app
3. Modele seus dados
4. Configure as rotas
5. Teste sua API
6. (Opcional) Configure seeders para dados iniciais