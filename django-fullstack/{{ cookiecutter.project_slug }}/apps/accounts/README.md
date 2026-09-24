# Accounts App

Autenticação por **sessão** do Django (sem DRF/JWT).

## Estrutura (responsabilidades separadas em pacotes)

```
apps/accounts/
├── models/            # modelos (vazio por padrão; use AbstractUser para estender)
├── views/             # views (auth.py: RegisterView, ProfileView)
├── forms/             # formulários (auth.py: UserRegisterForm)
├── services/          # regras de negócio (opcional)
├── selectors/         # consultas de leitura (opcional)
├── tests/             # testes
├── templates/
│   ├── registration/  # login.html, register.html, logged_out.html
│   └── accounts/      # profile.html
├── admin.py
├── apps.py
└── urls.py
```

## URLs

- `login/`, `logout/`, `register/`, `profile/`

## Fluxo

1. `GET/POST /register/` cria a conta e redireciona para `/login/`.
2. `POST /login/` autentica e redireciona para `home` (ou `next`).
3. `POST /logout/` encerra a sessão (Django 5 exige POST).
4. `/profile/` exige login (`@login_required`).

## Estender o usuário

Para adicionar campos, crie `models/user.py` com `AbstractUser`, exporte em
`models/__init__.py` e aponte `AUTH_USER_MODEL` em `core/settings/base.py`
**antes** da primeira migrate:

```python
# apps/accounts/models/user.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telefone = models.CharField(max_length=15, blank=True)
```

```python
# apps/accounts/models/__init__.py
from .user import User

__all__ = ["User"]
```

```python
# core/settings/base.py
AUTH_USER_MODEL = "accounts.User"
```

Depois inclua os campos em `UserRegisterForm`.
