from datetime import timedelta
from .base import BaseConfig
import os


class JWTConfig(BaseConfig):
    def __init__(
        self,
        access_token: timedelta = timedelta(minutes=5),
        refresh_token: timedelta = timedelta(days=1),
        signing_key: str = os.getenv("JWT_SECRET_KEY"),
    ):
        self.access_token_lifetime = access_token
        self.refresh_token_lifetime = refresh_token
        self.signing_key = signing_key
