"""
ASGI config for {{ cookiecutter.project_slug }} project.
"""

import os
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application


load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_asgi_application()
