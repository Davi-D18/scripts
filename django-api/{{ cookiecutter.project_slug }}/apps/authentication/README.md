# Authentication App (API)

Este app implementa autenticação baseada em JWT (JSON Web Tokens) com Django REST Framework + SimpleJWT.

## O que faz

- **Registro de usuários**: cria novas contas
- **Autenticação JWT**: login com username **ou** email + senha
- **Renovação de tokens**: renova o access token

## Estrutura

Este app usa arquivos únicos (diferente do scaffold gerado por `createapp`, que organiza em pastas por recurso):

- `schemas.py`: `UserSerializer` (registro) e `CustomerTokenObtainPairSerializer` (login por username/email)
- `controllers.py`: `RegisterView` e `CustomTokenObtainPairView`
- `urls.py`: rotas registradas em `/api/v1/auth/`

## Endpoints da API

- `POST /api/v1/auth/register/`: registra novo usuário
- `POST /api/v1/auth/login/`: autentica e retorna os tokens JWT
- `POST /api/v1/auth/login/refresh/`: renova o access token

## Personalizações comuns

### Adicionar campos ao usuário

O app usa o modelo de usuário padrão do Django. Para estender, crie um `models.py` neste app com um `AbstractUser` e aponte `AUTH_USER_MODEL` em `core/settings/base.py`:

```python
# apps/authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telefone = models.CharField(max_length=15, blank=True)
```

```python
# core/settings/base.py
AUTH_USER_MODEL = "authentication.User"
```

Depois inclua os novos campos em `UserSerializer`, dentro de `schemas.py`.

### Personalizar o payload do token JWT

Edite `schemas.py`:

```python
class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["name"] = user.get_full_name()
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        return token
```

### Alterar o tempo de expiração dos tokens

Os tempos ficam em `core/configs/libs/constants.py` (`JWT_TIMEOUTS`) e são aplicados via `JWTConfig` em `core/settings/development.py` e `core/settings/production.py`.
