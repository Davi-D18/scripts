### **1. Introdução ao ORM do Django**  
O Object-Relational Mapper (ORM) do Django permite definir estruturas de dados como classes Python (chamadas **models**) e mapeá-las automaticamente para tabelas em bancos de dados relacionais. Ele abstrai operações CRUD (Create, Read, Update, Delete) em métodos intuitivos, além de facilitar migrações de esquema e consultas complexas.  

**Principais vantagens**:  
- Elimina a necessidade de escrever SQL manualmente.  
- Mantém a compatibilidade com múltiplos bancos de dados (PostgreSQL, MySQL, SQLite, etc.).  
- Oferece segurança contra injeção de SQL.  
- Simplifica a criação de relacionamentos entre tabelas.  

---

### **2. Definindo um Modelo**  
Um modelo é uma classe Python que herda de `django.db.models.Model`. Cada atributo da classe representa um campo no banco de dados.  

**Exemplo**:  
```python
from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
```  

**Observações**:  
- O Django adiciona automaticamente um campo `id` como chave primária se nenhum campo for marcado com `primary_key=True`.  
- O nome da tabela no banco segue o padrão `<app_nome>_<model_nome>` (ex.: `app_pessoa`).  

---

### **3. Opções de Campos (Field Options)**  
Cada campo aceita argumentos para personalizar seu comportamento. As principais opções são:  

| Opção             | Descrição                                                                                   |
|--------------------|---------------------------------------------------------------------------------------------|
| **`null`**         | Permite `NULL` no banco (padrão: `False`). Não use para campos de texto (prefira `blank`).  |
| **`blank`**        | Permite valor vazio em formulários (padrão: `False`).                                       |
| **`choices`**      | Lista de opções pré-definidas (ex.: `[('M', 'Masculino'), ('F', 'Feminino')]`).            |
| **`default`**      | Valor padrão (evite objetos mutáveis como listas; use `lambda` ou funções).                 |
| **`primary_key`**  | Define o campo como chave primária (substitui o `id` automático).                           |
| **`unique`**       | Garante que todos os valores sejam únicos na tabela.                                        |
| **`verbose_name`** | Nome legível para o campo (exibido no admin do Django).                                     |

**Dica**:  
- `null=True` + `blank=True`: Campo opcional no formulário e no banco.  
- `blank=True` (sem `null`): Campo opcional no formulário, mas o banco armazena string vazia.  

---

### **4. Tipos de Campos Principais**  

#### **4.1 Campos de Texto**  
- **`CharField`**: Texto curto (exige `max_length`).  
- **`TextField`**: Texto longo (sem limite no banco, mas `max_length` afeta widgets de formulário).  
- **`EmailField`**: Valida formato de e-mail.  
- **`SlugField`**: Texto para URLs (aceita apenas letras, números, hífens e underscores).  

#### **4.2 Campos Numéricos**  
- **`IntegerField`**, **`DecimalField`**: Para inteiros e decimais de precisão fixa.  
- **`PositiveIntegerField`**: Aceita apenas valores ≥ 0.  

#### **4.3 Campos de Data/Hora**  
- **`DateField`**, **`DateTimeField`**: Armazenam datas e horários.  
  - `auto_now=True`: Atualiza automaticamente ao salvar o objeto (útil para `última_modificação`).  
  - `auto_now_add=True`: Define apenas na criação (útil para `data_criacao`).  

#### **4.4 Campos de Relacionamento**  
- **`ForeignKey`**: Relação muitos-para-um (ex.: Um autor tem muitos livros). **Obrigatório:** `on_delete` (ex.: `models.CASCADE`).  
- **`ManyToManyField`**: Relação muitos-para-muitos (ex.: Um livro pertence a várias categorias).  
- **`OneToOneField`**: Relação um-para-um (ex.: Perfil de usuário).  

#### **4.5 Campos Especiais**  
- **`FileField`**, **`ImageField`**: Armazenam arquivos/imagens (para `ImageField`, instale a biblioteca `Pillow`).  
- **`UUIDField`**: Armazena UUIDs (identificadores únicos universais).  
- **`JSONField`**: Armazena dados JSON nativos (suportado em PostgreSQL, SQLite ≥ 3.9).  

---

### **5. Exemplos Práticos**  

#### **Modelo com Validações e Relacionamentos**  
```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Produto(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Produto",
        help_text="Insira o nome completo do produto",
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
    )
    CATEGORIAS = [
        ("ELE", "Eletrônicos"),
        ("ROUP", "Roupas"),
        ("ALI", "Alimentos"),
    ]
    categoria = models.CharField(max_length=4, choices=CATEGORIAS, default="ELE")
    
    class Status(models.TextChoices):
        DISPONIVEL = "D", "Disponível"
        ESGOTADO = "E", "Esgotado"
    
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.DISPONIVEL,
    )
    fornecedor = models.ForeignKey(
        "Fornecedor",
        on_delete=models.CASCADE,
        related_name="produtos",
    )
```  

**Explicações Adicionais**:  
- **`choices`**: Pode usar listas de tuplas ou enums (como `TextChoices`).  
- **`validators`**: Adicione validações customizadas (ex.: `MinValueValidator`).  

---

### **6. Configurações Avançadas (Classe Meta)**  
Personalize o comportamento do modelo com a classe `Meta`:  

```python
class Produto(models.Model):
    # ... campos ...
    
    class Meta:
        db_table = "produtos"  # Nome personalizado da tabela
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["-preco"]  # Ordena por preço decrescente por padrão
        constraints = [
            models.UniqueConstraint(
                fields=["nome", "fornecedor"], 
                name="nome_fornecedor_unico"
            )
        ]
```  

**Opções Comuns**:  
- **`ordering`**: Define a ordem padrão das queries (`['-campo']` para decrescente).  
- **`unique_together`**: Define unicidade combinada de campos (substituído por `constraints` em versões recentes).  
- **`indexes`**: Cria índices para otimizar consultas.  

---

### **7. Erros Comuns e Boas Práticas**  

#### **Erros Frequentes**  
1. **Esquecer `on_delete` em `ForeignKey`**:  
   ```python
   # ❌ Incorreto (gera erro)
   fornecedor = models.ForeignKey("Fornecedor")
   
   # ✅ Correto
   fornecedor = models.ForeignKey("Fornecedor", on_delete=models.CASCADE)
   ```  

2. **Usar `default` com objetos mutáveis**:  
   ```python
   # ❌ Risco: Todas as instâncias compartilham a mesma lista!
   tags = models.JSONField(default=[])
   
   # ✅ Correto (use uma função)
   tags = models.JSONField(default=list)
   ```  

#### **Boas Práticas**  
- Use `related_name` em relacionamentos para evitar conflitos:  
  ```python
  autor = models.ForeignKey("Autor", on_delete=models.CASCADE, related_name="livros")
  ```  
- Evite `null=True` para campos de texto (prefira `blank=True` + valor padrão).  

---

### **8. Migrações**  
Após definir ou alterar modelos, gere e aplique migrações:  
```bash
python manage.py makemigrations
python manage.py migrate
```  

**Dica**: Revise o SQL gerado com `python manage.py sqlmigrate <app> <migration_number>`.  

---

**Observações Finais**:  
- O Django não suporta chaves primárias compostas nativamente. Use `UniqueConstraint` para simular esse comportamento.  
- Para campos computados (ex.: soma de valores), considere usar anotações (`annotate()`) ou `GeneratedField` (Django 4.2+).  

Consulte a [documentação oficial](https://docs.djangoproject.com/) para detalhes avançados!


### **3. Relacionamentos Avançados**  

#### **Many-to-Many com Through**  
```python
class Autor(models.Model):
    nome = models.CharField(max_length=100)

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor, through='AutorLivro')

class AutorLivro(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_contrato = models.DateField()  # Campo adicional na relação
```  
**Uso**:  
```python
livro = Livro.objects.get(id=1)
autores = livro.autores.all()  # Acessa autores via tabela intermediária
```  

---

### **4. Métodos de Modelo**  
Adicione lógica personalizada diretamente nos models:  

#### **Método para Calcular Idade**  
```python
from django.utils import timezone

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    def idade(self):
        hoje = timezone.now().date()
        return (hoje - self.data_nascimento).days // 365
```  

#### **Sobrescrevendo Save()**  
```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.titulo)
    super().save(*args, **kwargs)
```  

---

### **5. Managers Customizados**  
Crie consultas pré-definidas para reutilização:  

```python
class LivroManager(models.Manager):
    def disponiveis(self):
        return self.filter(estoque__gt=0)

    def por_autor(self, autor_nome):
        return self.filter(autor__nome__icontains=autor_nome)

class Livro(models.Model):
    # ... campos ...
    objects = LivroManager()  # Substitui o manager padrão
```  

**Uso**:  
```python
livros_disponiveis = Livro.objects.disponiveis()
livros_tolkien = Livro.objects.por_autor("Tolkien")
```  

---

### **6. Validação de Modelo**  
Valide dados antes de salvar:  

```python
from django.core.exceptions import ValidationError

class Produto(models.Model):
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.preco < 0:
            raise ValidationError("Preço não pode ser negativo!")
```  
**Importante**: Chame `full_clean()` antes de salvar no código ou use `ModelForm`.

---

### **7. Classe Meta Avançada**  
Personalize o comportamento do modelo:  

```python
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-preco']  # Ordena do mais caro para o mais barato
        verbose_name_plural = "Produtos"
        indexes = [
            models.Index(fields=['nome'], name='idx_nome')  # Índice no campo nome
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(preco__gte=0),
                name="preco_nao_negativo"
            )
        ]
```  

---

### **8. Herança de Modelos**  

#### **Modelo Abstrato (Reuso de Campos)**  
```python
class Auditoria(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Não cria tabela

class Postagem(Auditoria):
    titulo = models.CharField(max_length=200)
```  
**Resultado**: `Postagem` herda `criado_em` e `atualizado_em`.

---

### **9. Sinais (Signals)**  
Execute ações antes/depois de eventos:  

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Produto)
def atualizar_estoque(sender, instance, created, **kwargs):
    if created:
        print(f"Novo produto criado: {instance.nome}")
```  

---

### **10. Consultas Complexas**  

#### **Agregação e Anotação**  
```python
from django.db.models import Avg, F

# Média de preços dos produtos por categoria
categorias = Produto.objects.values('categoria').annotate(preco_medio=Avg('preco'))

# Aumentar preço em 10% para todos
Produto.objects.update(preco=F('preco') * 1.10)
```  

---

### **11. Boas Práticas e Dicas**  

1. **Evite N+1 Queries**:  
   ```python
   # Ruim (1 query por autor)
   for livro in Livro.objects.all():
       print(livro.autor.nome)

   # Bom (1 query com join)
   for livro in Livro.objects.select_related('autor').all():
       print(livro.autor.nome)
   ```  

2. **Transações**:  
   ```python
   from django.db import transaction

   with transaction.atomic():
       produto = Produto.objects.select_for_update().get(id=1)
       produto.estoque -= 1
       produto.save()
   ```  

3. **Índices para Campos Usados em Filtros**:  
   ```python
   class Cliente(models.Model):
       nome = models.CharField(max_length=100, db_index=True)  # Índice criado
   ```  

---

### **12. Exemplo Completo: Rede Social**  
```python
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Postagem(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    curtidas = models.ManyToManyField(Usuario, related_name='postagens_curtidas')
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def total_curtidas(self):
        return self.curtidas.count()

class Comentario(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
```  

**Uso**:  
```python
postagem = Postagem.objects.get(id=1)
postagem.curtidas.add(usuario)  # Adiciona curtida
print(postagem.total_curtidas())  # Exibe 1
```  

---

### **13. Recursos Adicionais**  
- **`F()`**: Para operações atômicas (ex.: `F('visualizacoes') + 1`).  
- **`Q()`**: Para consultas complexas com `OR`/`AND`.  
- **`Prefetch`**: Otimiza `ManyToMany` ou relacionamentos reversos.  