from django.contrib import admin
from django.urls import path, include
from django.conf import settings
{%- if cookiecutter.use_documentation == "yes" %}
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
{% endif %}

urlpatterns = [
   path('admin/', admin.site.urls),
   # path('api/v1/', include('apps.nome-app.urls')),
   {%- if cookiecutter.use_authentication == "yes" %}
   path('api/v1/auth/', include('apps.authentication.urls')),
   {%- endif %}
   {%- if cookiecutter.use_documentation == "yes" %}
   path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
   path("docs/", SpectacularSwaggerView.as_view(), name="schema-swagger-ui"),
   {%- endif %}
]

# Debug Toolbar URLs (apenas em desenvolvimento)
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            path('debug/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
