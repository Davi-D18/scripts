# Authentication App

Este app implementa um sistema de autenticação baseado em JWT (JSON Web Tokens)

## O que faz

- **Registro de usuários**: Permite criar novas contas
- **Autenticação JWT**: Login com username/email e senha
- **Renovação de tokens**: Sistema seguro para manter sessões ativas

## Endpoints da API

- `POST /register/`: Registra novo usuário
- `POST /login/`: Autentica e retorna tokens JWT
- `POST /login/refresh/`: Renova token de acesso expirado

## Personalizações comuns

### Adicionar campos ao usuário

Edite `models/auths.py` para estender o modelo de usuário:

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Adicione campos personalizados
    telefone = models.CharField(max_length=15, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
```

Atualize `schemas/auth_schema.py` para incluir os novos campos:

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'telefone', 'data_nascimento']
        extra_kwargs = {'password': {'write_only': True}}
```

### Personalizar payload do token JWT

Edite `schemas/auth_schema.py` para modificar o payload do token:

```python
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Adicione claims personalizadas
        token['name'] = user.get_full_name()
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        
        return token
```

### Alterar tempo de expiração dos tokens

Edite as configurações em `core/settings/base.py`:

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Padrão: 15 minutos
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Padrão: 1 dia
}
```