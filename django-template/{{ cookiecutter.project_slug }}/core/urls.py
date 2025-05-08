from django.contrib import admin
from django.urls import path, include
{%- if cookiecutter.use_authentication == "yes" %}
from rest_framework_simplejwt import views as jwt_views
{%- endif %}
{%- if cookiecutter.use_documentation == "yes" %}
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="{{ cookiecutter.project_name }} API",
      default_version='v1',
      description="{{ cookiecutter.project_name }} API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
{% endif %}

urlpatterns = [
path('admin/', admin.site.urls),
# path('api/v1/', include('apps.nome-app.urls')),
{%- if cookiecutter.use_authentication == "yes" %}
path('api/v1/token/', jwt_views.TokenObtainPairView.as_view(),
			name='token_obtain_pair'),
path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(),
			name='token_refresh'),
{%- endif %}
{%- if cookiecutter.use_documentation == "yes" %}
path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
{%- endif %}
]
