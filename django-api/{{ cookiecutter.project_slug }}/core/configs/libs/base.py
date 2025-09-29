from typing import Dict, Any


class BaseConfig:
    def as_dict(self) -> Dict[str, Any]:
        """Converte atributos públicos em dicionário com chaves UPPER_CASE"""
        config = {}
        for key in dir(self):
            if not key.startswith("_") and not callable(getattr(self, key)):
                value = getattr(self, key)
                # Converte snake_case para UPPER_CASE
                config_key = key.upper()
                config[config_key] = value
        return config

    def override(self, **kwargs) -> "BaseConfig":
        """Sobrescreve atributos existentes. Se o atributo atual for lista/dict,
        e o novo valor for do mesmo tipo, faz merge ao invés de substituir."""
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError(
                    f"'{self.__class__.__name__}' não tem o atributo '{key}'"
                )

            current = getattr(self, key)
            # merge para listas
            if isinstance(current, list) and isinstance(value, list):
                # evita duplicatas simples (opcional)
                merged = [*current]
                for item in value:
                    if item not in merged:
                        merged.append(item)
                setattr(self, key, merged)
            # merge para dicts
            elif isinstance(current, dict) and isinstance(value, dict):
                merged = {**current, **value}
                setattr(self, key, merged)
            else:
                # substitui normalmente
                setattr(self, key, value)
        return self
