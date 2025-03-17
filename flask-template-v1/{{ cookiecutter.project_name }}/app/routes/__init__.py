from .news import news_bp
{% if cookiecutter.use_auth == "y" %}
from .auth import auth_bp
{% endif %}
