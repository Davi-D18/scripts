from typing import Mapping

from products_api.core.messages.env import (
    ENVIRONMENT_INVALID,
    ENVIRONMENT_NOT_DEFINED,
)

from .boot import BootSettings
from .development import DevelopmentSettings
from .production import ProductionSettings

boot_settings = BootSettings()

ALL_ENVIRONMENTS: Mapping[str, type] = {
    'DEVELOPMENT': DevelopmentSettings,
    'PRODUCTION': ProductionSettings,
}

env = boot_settings.ENVIRONMENT

if not env:
    raise ValueError(ENVIRONMENT_NOT_DEFINED)

env_up = env.upper()

try:
    Settings = ALL_ENVIRONMENTS[env_up]
except KeyError:
    raise ValueError(ENVIRONMENT_INVALID)

settings = Settings()

__all__ = ['Settings', 'settings']
