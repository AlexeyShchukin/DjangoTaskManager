
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    info=openapi.Info(
        title="App API",
        default_version="v1",
        description="Simple Swagger for App API",
        terms_of_service="",
        contact=openapi.Contact(name='Alexey', url=''),
        license=openapi.License(name='MIT License', url=''),
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(
            cache_timeout=0),
            name='api-schema'

    ),
    path(
        'swagger/',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0
        )
    ),
    path(
        'redoc/',
        schema_view.with_ui(
            'redoc',
            cache_timeout=0
        )
    ),
    path(
        'api/v1/',
        include('src.routes')
    ),
]
