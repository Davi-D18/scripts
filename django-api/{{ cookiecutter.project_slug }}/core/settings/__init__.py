import os
import sys
from importlib import import_module

# Determina qual ambiente carregar
DJANGO_ENV = os.getenv("DJANGO_ENV", "development")

# Mapeamento de classes de configuração
SETTINGS_MODULES = {
    "development": "core.settings.development.DevelopmentSettings",
    "production": "core.settings.production.ProductionSettings",
}

# Importa dinamicamente a classe de configuração
module_path, class_name = SETTINGS_MODULES[DJANGO_ENV].rsplit(".", 1)
settings_module = import_module(module_path)
settings_class = getattr(settings_module, class_name)

# Cria uma instância da classe
SETTINGS = settings_class()

# Exporta todos os atributos UPPERCASE para o módulo
for attr_name in dir(SETTINGS):
    if attr_name.isupper():
        setattr(sys.modules[__name__], attr_name, getattr(SETTINGS, attr_name))
