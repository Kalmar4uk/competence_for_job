import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


urlpatterns = [
    path('', include("matrix.urls")),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('api/', include("api.urls"))
]

handler500 = "matrix.pages.server_error"
handler404 = "matrix.pages.page_not_found"
handler403csrf = "matrix.pages.csrf_permission_denied"

schema_view = get_schema_view(
   openapi.Info(
      title="Matrix API",
      default_version='v1',
      description="Документация",
      contact=openapi.Contact(email="admin@mail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
       cache_timeout=0), name='schema-json'
    ),
   re_path(r'^api/swagger/$', schema_view.with_ui(
       'swagger', cache_timeout=0), name='schema-swagger-ui'
    ),
]

if settings.DEBUG:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
