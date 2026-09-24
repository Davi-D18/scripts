from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic import TemplateView


def favicon(request):
    """Redireciona /favicon.ico para o arquivo estático (resolvido na requisição)."""
    return redirect(static("favicon.ico"), permanent=True)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.ico", favicon),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    {%- if cookiecutter.use_authentication == "yes" %}
    path("", include("apps.accounts.urls")),
    {%- endif %}
]

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    except ImportError:
        pass
