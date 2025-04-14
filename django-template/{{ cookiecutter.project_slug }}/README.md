## 1. Criando um novo app
Use o comando personalizado para criar a estrutura inicial:
```bash
python manage.py createapp nome-app
```
Isso criará:
```
apps/meu_app/
├── controllers/
├── models/
├── schemas/
├── services/
├── routes/
├── migrations/
└── tests/
```

## 2. Configurando Models
Edite `apps/meu_app/models/`:
```python
from django.db import models

# Exemplo de model
class Produtos(models.Model):
    nome = models.CharField(max_length=100) 
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Produto'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome
```

Parâmetros comuns de models:
- `CharField`: max_length
- `IntegerField`: default, choices
- `DecimalField`: max_digits, decimal_places
- `DateTimeField`: auto_now (atualiza sempre), auto_now_add (só na criação)
- `ForeignKey`: on_delete

## 3. Configurando Schemas (Serializers)
Edite `apps/meu_app/schemas/produto_schema.py`:
```python
from rest_framework import serializers
from apps.meu_app.models.produtos import Produtos

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = ['id', 'nome', 'preco', 'estoque'] # ou coloque __all__ para serializar todos os campos
        extra_kwargs = {
            'preco': {'min_value': 0},
            'estoque': {'min_value': 0}
        }
```

## 4. Configurando Controllers (Views)
```python
from rest_framework import viewsets
from apps.meu_app.schemas.produto_schema import ProdutoSerializer # Serializador
from apps.meu_app.models.produtos import Produtos # Tabela no banco

class ProdutosViewSet(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = ProdutoSerializer
```

## 5. Configurando Rotas
Edite `apps/meu_app/routes/`:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.meu_app.controllers.produtos_controller import ProdutosViewSet

router = DefaultRouter()
router.register('produtos', ProdutosViewSet)

urlpatterns = [
    path('', include(router.urls))
]
```

## 6. Registrando URLs no Projeto
No `urls.py` principal do projeto:
```python
from django.urls import include, path

urlpatterns = [
    path('api/v1/', include('apps.meu_app.urls')),
]
```

## 7. Registrar o app em core
Vá para o diretório `core/settings/base.py` e registre o app em:
```python
INSTALLED_APPS = [
    'apps.meuapp'
]
```

## 8. Executando Migrações
```bash
python manage.py makemigrations meu_app
python manage.py migrate
```

## 9. Testando a API
A API estará disponível em:
- GET `/api/produtos/` - Lista todos
- POST `/api/produtos/` - Cria novo
- GET `/api/produtos/{id}/` - Detalhes
- PUT/PATCH `/api/produtos/{id}/` - Atualiza
- DELETE `/api/produtos/{id}/` - Exclui

## 9. Adicionando Lógica de Negócio (caso precise)
Edite `apps/meu_app/services/produtos_service.py`:
```python
from apps.meu_app.models.produtos import Produtos

class ProdutoService:
    @classmethod
    def atualizar_estoque(cls, produto_id, quantidade):
        produto = Produtos.objects.get(id=produto_id)
        produto.estoque += quantidade
        produto.save()
        return produto
```

## 10. Customizando Querysets
No controller, você pode sobrescrever métodos:
```python
class ProdutosViewSet(ModelViewSet):
    # ...
    
    def get_queryset(self):
        return Produtos.objects.filter(estoque__gt=0)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
```

## Parâmetros Comuns no DRF:
- `fields`: Lista de campos a serem serializados
- `read_only_fields`: Campos somente leitura
- `extra_kwargs`: Configurações adicionais por campo
- `pagination_class`: Tipo de paginação
- `permission_classes`: Controle de acesso
- `filter_backends`: Filtros de pesquisa

## Dicas Rápidas:
1. Sempre registre o app em `settings.INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'apps.meu_app'
]
```

2. Para testar a API use:
```bash
python manage.py runserver
```

3. Acesse a interface web do DRF em:
`http://localhost:8000/api/produtos/`

## Django-Admin
```python
from django.contrib import admin
from cars.models import Brand, Car 


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at',) 
    search_fields = ('name',)


class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'brand__name', 'color',
								    'factory_year', 'model_year', 'created_at',)
    search_fields = ('model',)
    list_filter = ('brand',)


admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)

```

No **Django Admin**, você personaliza a forma como seus modelos aparecem na interface de administração definindo atributos na sua classe `ModelAdmin`. Os mais comuns:

| Propriedade           | O que faz                                                                                                                                                                                                                                                                                  |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **list_display**      | Tupla de campos (ou métodos) que serão exibidos como colunas na **lista** de objetos daquele modelo. Pode conter nomes de campos do próprio modelo (`'id'`, `'name'`) ou atravessar relações (`'brand__name'`).                                                                                 |
| **search_fields**     | Tupla de campos que serão pesquisáveis pela **barra de busca** no topo da lista. Suporta lookup `icontains` por padrão. Para relações, use `__` (ex.: `'brand__name'`).                                                                                                                     |
| **list_filter**       | Tupla de campos que geram filtros na barra lateral (sidebar). Ideal para campos com escolhas fixas (`choices`), `BooleanField`, `DateField/DateTimeField`, ou FK/M2M.                                                                                                                          |
| **ordering**          | Tupla ou lista que define a ordenação padrão dos objetos na listagem. Ex.: `ordering = ('-created_at', 'name')`.                                                                                                                                                                            |
| **list_per_page**     | Número de itens por página na listagem (padrão: 100). Ex.: `list_per_page = 25`.                                                                                                                                                                                                           |
| **list_editable**     | Campos que podem ser editados diretamente na listagem. Atenção: não pode incluir o primeiro campo (link para o detalhe). Ex.: `list_editable = ('color',)`.                                                                                                                               |
| **date_hierarchy**    | Adiciona uma barra de navegação por data no topo, baseada em um campo `DateField` ou `DateTimeField`. Ex.: `date_hierarchy = 'created_at'`.                                                                                                                                                  |
| **list_select_related** | Define campos de FK para usar `select_related()` na query, reduzindo queries ao buscar objetos relacionados. Ex.: `list_select_related = ('brand',)`.                                                                                                                                       |
| **prepopulated_fields** | Preenche automaticamente um campo a partir de outro (útil para slugs). Dicionário: `{ 'slug': ('name',) }`.                                                                                                                                                                                 |
| **raw_id_fields**     | Exibe um campo FK como input de ID em vez de dropdown — bom quando há milhares de objetos. Tupla de nomes de campos FK.                                                                                                                                                                      |
| **autocomplete_fields** | Transforma FK/M2M em um campo de busca autocomplete (requer definir `search_fields` no ModelAdmin do modelo relacionado).                                                                                                                                                                    |
| **filter_horizontal / filter_vertical** | Para campos M2M, exibe um widget de seleção múltipla com caixas lado a lado (horizontal) ou empilhadas (vertical).                                                                                                                                                |
| **fieldsets**         | Organiza os campos no formulário de edição em grupos e colunas. Ex.:  
```python
fieldsets = (
    ('Dados principais', {
        'fields': ('name', 'slug')
    }),
    ('Informações adicionais', {
        'classes': ('collapse',),
        'fields': ('description', 'created_at'),
    }),
)
```