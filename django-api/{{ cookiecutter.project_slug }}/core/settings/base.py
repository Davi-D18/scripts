import os
from pathlib import Path
from decouple import config
from core.configs.libs.drf import DRFConfig
{%- if cookiecutter.use_documentation == "yes" %}
from core.configs.libs.swagger import SwaggerConfig
{%- endif %}


class BaseSettings:
    """
    Configurações base do projeto.
    """
    ENVIRONMENT_NAME = "Base"
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    SECRET_KEY = config('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production')

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        {%- if cookiecutter.use_authentication == "yes" %}
        'rest_framework_simplejwt',
        {%- endif %}
        {%- if cookiecutter.use_documentation == "yes" %}
        'drf_spectacular',
        {%- endif %}
        'corsheaders',
        'core',
        'django_db_logger',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ]

    ROOT_URLCONF = 'core.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'core.wsgi.application'

    DATABASES = {
        'development': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'database.db'
        },
        {%- if cookiecutter.banco_de_dados != "sqlite3" %}
        'production': {
            'ENGINE': 'django.db.backends.{{cookiecutter.banco_de_dados}}',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
        {%- endif %}
    }

    {%- if cookiecutter.use_documentation == "yes" %}
    REST_FRAMEWORK = {
        **DRFConfig().as_dict(),
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    }
    {%- else %}
    REST_FRAMEWORK = DRFConfig().as_dict()
    {%- endif %}

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

    LANGUAGE_CODE = 'pt-br'
    TIME_ZONE = 'America/Sao_Paulo'

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    EMAIL_HOST = config('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', 587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', 'True', cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', '')

    {%- if cookiecutter.use_documentation == "yes" %}
    SPECTACULAR_SETTINGS = SwaggerConfig(
        title="APi {{ cookiecutter.project_name }}",
        description="Documentação da API",
    ).as_dict()
    {%- endif %}

    def __init__(self):
        self.select_database()
        self.print_environment_info()

    def select_database(self):
        """Seleciona a configuração de banco"""
        if self.DATABASE_ALIAS not in self.DATABASES:
            available = list(self.DATABASES.keys())
            raise ValueError(
                f"Alias '{self.DATABASE_ALIAS}' não encontrado. "
                f"Configurações disponíveis: {available}"
            )

        self.DATABASES = {"default": self.DATABASES[self.DATABASE_ALIAS]}

    def print_environment_info(self):
        """Exibe informações do ambiente no console"""
        print("\n" + "=" * 30)

        if self.ENVIRONMENT_NAME.upper() == "PRODUCTION":
            print(f"⚙️  Ambiente: {self.ENVIRONMENT_NAME}")
        else:
            print(f"⚙️  Ambiente: {self.ENVIRONMENT_NAME}")
            print(f"🔧 DEBUG: {getattr(self, 'DEBUG', 'Não definido')}")
            print(
                f"🗄️  Database: {self.DATABASES['default']['ENGINE'].split('.')[-1].title()}"
            )
        print("=" * 30 + "\n")
