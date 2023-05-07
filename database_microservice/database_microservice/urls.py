from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Video Perception analyzer Database API",
        default_version='v1',
        description="Video Perception analyzer Database API",
        contact=openapi.Contact(email="aryan.jadon@sjsu.edu"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # url patterns
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # documentation
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # documentation

    path('videos-api/', include('videos_api.urls')),  # videos api
    path('users-api/', include('users_api.urls')),  # users api
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
