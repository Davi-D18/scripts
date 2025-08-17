from typing import Dict, Any

class BaseConfig:
    def as_dict(self) -> Dict[str, Any]:
        """Converte atributos públicos em dicionário com chaves UPPER_CASE"""
        config = {}
        for key in dir(self):
            if not key.startswith('_') and not callable(getattr(self, key)):
                value = getattr(self, key)
                # Converte snake_case para UPPER_CASE
                config_key = key.upper()
                config[config_key] = value
        return config
    
    def override(self, **kwargs) -> "BaseConfig":
        """Sobrescreve atributos existentes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' não tem o atributo '{key}'")
        return self