**Guia Ampliado: Django REST Framework (DRF) com Práticas Avançadas e Exemplos Reais**

---

### **1. Introdução ao Django REST Framework (DRF)**  
O DRF é um toolkit para construir APIs RESTful robustas em Django. Além das funcionalidades básicas, oferece recursos avançados como:  
- **Documentação automática** (OpenAPI/Swagger)  
- **Autenticação via JWT**  
- **Serialização aninhada** (relacionamentos complexos)  
- **Testes automatizados**  
- **Caching** e **Otimizações de desempenho**

---

### **2. Configuração Avançada**  
#### **Configurações Recomendadas em `settings.py`**  
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Documentação
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
    'EXCEPTION_HANDLER': 'api.utils.custom_exception_handler',  # Customização de erros
}
```

#### **CORS (Cross-Origin Resource Sharing)**  
Instale `django-cors-headers` para permitir acesso de outros domínios:  
```python
# settings.py
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE
CORS_ALLOWED_ORIGINS = ["https://seusite.com"]
```

---

### **3. Serializers Avançados**  
#### **Validação Customizada**  
```python
from rest_framework import serializers

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['nome', 'preco']

    def validate_preco(self, value):
        if value < 0:
            raise serializers.ValidationError("Preço não pode ser negativo!")
        return value
```

#### **Campos Relacionais Aninhados**  
```python
class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nome']

class LivroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer()  # Serialização aninhada

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'publicado_em']
```

#### **Campos Dinâmicos**  
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {
            'password': {'write_only': True}  # Campo não é retornado na resposta
        }
```

---

### **4. Viewsets e Ações Customizadas**  
#### **Customizando ViewSets**  
```python
from rest_framework.decorators import action
from rest_framework.response import Response

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    @action(detail=True, methods=['post'])
    def publicar(self, request, pk=None):
        livro = self.get_object()
        livro.publicado = True
        livro.save()
        return Response({'status': 'Livro publicado!'})
```

**URL Gerada**: `/livros/{id}/publicar/`

---

### **5. Autenticação com JWT**  
#### **Configuração do Simple JWT**  
1. Instale:  
```bash
pip install djangorestframework-simplejwt
```

2. Em `settings.py`:  
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

3. Rotas para tokens:  
```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

### **6. Filtragem e Busca Avançada**  
#### **Filtragem por Intervalo de Datas**  
```python
import django_filters

class PedidoFilter(django_filters.FilterSet):
    data_min = django_filters.DateFilter(field_name='data_criacao', lookup_expr='gte')
    data_max = django_filters.DateFilter(field_name='data_criacao', lookup_expr='lte')

    class Meta:
        model = Pedido
        fields = ['status', 'data_min', 'data_max']

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    filterset_class = PedidoFilter
```

**Exemplo de Uso**:  
`GET /pedidos/?data_min=2023-01-01&data_max=2023-12-31`

---

### **7. Paginação Customizada**  
```python
from rest_framework.pagination import PageNumberPagination

class LargeResultsPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    pagination_class = LargeResultsPagination
```

---

### **8. Testes com Factory Boy**  
#### **Criando Dados de Teste**  
1. Instale:  
```bash
pip install factory_boy
```

2. Crie factories:  
```python
import factory
from .models import Livro

class LivroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Livro

    titulo = factory.Faker('sentence')
    autor = factory.Faker('name')
```

3. Use nos testes:  
```python
from rest_framework.test import APITestCase

class LivroAPITest(APITestCase):
    def setUp(self):
        self.livro = LivroFactory.create()

    def test_listar_livros(self):
        response = self.client.get('/livros/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
```

---

### **9. Documentação da API com drf-spectacular**  
1. Instale:  
```bash
pip install drf-spectacular
```

2. Configure `settings.py`:  
```python
INSTALLED_APPS += ['drf_spectacular']
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API de Livros',
    'DESCRIPTION': 'Documentação completa da API',
    'VERSION': '1.0.0',
}
```

3. Adicione URLs:  
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
```

---

### **10. Boas Práticas em Produção**  
#### **Segurança**  
- Use HTTPS em produção  
- Limite tentativas de login com `django-axes`  
- Esconda chaves secretas com `python-dotenv`  

#### **Desempenho**  
```python
# Use select_related e prefetch_related para otimizar queries
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related('cliente').prefetch_related('itens')
```

#### **Logging**  
Configure `LOGGING` em `settings.py` para monitorar erros e acessos.

---

### **11. Exemplo Completo: API de Blog**  
#### **Modelos**  
```python
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    publicado_em = models.DateTimeField(auto_now_add=True)

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
```

#### **Serializers**  
```python
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'texto', 'autor', 'post']

class PostSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'titulo', 'conteudo', 'autor', 'comentarios']
```

#### **Viewsets**  
```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related('comentarios')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def comentar(self, request, pk=None):
        post = self.get_object()
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, autor=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

**Endpoints**:  
- `GET /posts/`: Lista posts  
- `POST /posts/{id}/comentar/`: Adiciona comentário  

---

### **12. Erros Comuns e Soluções**  
#### **Problema: N+1 Queries**  
**Solução**: Use `select_related` (FK) e `prefetch_related` (M2M):  
```python
queryset = Post.objects.select_related('autor').prefetch_related('comentarios')
```

#### **Problema: Serialização Lenta**  
**Solução**: Use `SerializerMethodField` para cálculos leves ou otimize no banco:  
```python
class PostSerializer(serializers.ModelSerializer):
    total_comentarios = serializers.SerializerMethodField()

    def get_total_comentarios(self, obj):
        return obj.comentarios.count()
```

---

### **13. Recursos Adicionais**  
- **WebSockets**: Use `django-channels` para APIs em tempo real.  
- **Upload de Arquivos**: Use `FileField` no serializer e configure `MEDIA_ROOT`.  
- **Cache**: Use `@method_decorator(cache_page(60*15))` em views.  
- **Monitoramento**: Integre com Sentry ou New Relic.  

Consulte a [documentação oficial do DRF](https://www.django-rest-framework.org/) para explorar mais recursos! 🚀