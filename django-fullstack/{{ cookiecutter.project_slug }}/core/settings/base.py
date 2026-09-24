from pathlib import Path

from decouple import config


class BaseSettings:
    """Configurações comuns a todos os ambientes."""

    ENVIRONMENT_NAME = "Base"
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    SECRET_KEY = config("DJANGO_SECRET_KEY", "django-insecure-change-this-in-production")
    DEBUG = False

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "core",
        "django_db_logger",
        {%- if cookiecutter.use_authentication == "yes" %}
        "apps.accounts",
        {%- endif %}
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "core.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "core.wsgi.application"
    ASGI_APPLICATION = "core.asgi.application"

    DATABASES = {
        "development": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "database.db",
        },
        {%- if cookiecutter.database == "sqlite3" %}
        "production": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": config("DB_NAME", str(BASE_DIR / "production.db")),
        },
        {%- elif cookiecutter.database == "postgresql" %}
        "production": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME", "app"),
            "USER": config("DB_USER", "app"),
            "PASSWORD": config("DB_PASSWORD", "app"),
            "HOST": config("DB_HOST", "localhost"),
            "PORT": config("DB_PORT", "5432"),
        },
        {%- else %}
        "production": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": config("DB_NAME", "app"),
            "USER": config("DB_USER", "app"),
            "PASSWORD": config("DB_PASSWORD", "app"),
            "HOST": config("DB_HOST", "localhost"),
            "PORT": config("DB_PORT", "3306"),
        },
        {%- endif %}
    }

    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_DIRS = [BASE_DIR / "static"]
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

    {%- if cookiecutter.use_authentication == "yes" %}
    LOGIN_URL = "login"
    LOGIN_REDIRECT_URL = "home"
    LOGOUT_REDIRECT_URL = "home"
    {%- endif %}

    LANGUAGE_CODE = "{{ cookiecutter.language_code }}"
    TIME_ZONE = "{{ cookiecutter.timezone }}"
    USE_I18N = True
    USE_TZ = True

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    EMAIL_HOST = config("EMAIL_HOST", "localhost")
    EMAIL_PORT = config("EMAIL_PORT", 25, cast=int)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", False, cast=bool)
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", "webmaster@localhost")

    def __init__(self):
        self.select_database()
        self.print_environment_info()

    def select_database(self):
        """Seleciona a configuração de banco conforme o ambiente."""
        if self.DATABASE_ALIAS not in self.DATABASES:
            available = list(self.DATABASES.keys())
            raise ValueError(
                f"Alias '{self.DATABASE_ALIAS}' não encontrado. "
                f"Configurações disponíveis: {available}"
            )
        self.DATABASES = {"default": self.DATABASES[self.DATABASE_ALIAS]}

    def print_environment_info(self):
        """Exibe informações do ambiente no console."""
        print("\n" + "=" * 30)
        print(f"Ambiente: {self.ENVIRONMENT_NAME}")
        if self.ENVIRONMENT_NAME.upper() != "PRODUCTION":
            print(f"DEBUG: {getattr(self, 'DEBUG', 'Não definido')}")
            engine = self.DATABASES["default"]["ENGINE"].split(".")[-1]
            print(f"Database: {engine}")
        print("=" * 30 + "\n")
