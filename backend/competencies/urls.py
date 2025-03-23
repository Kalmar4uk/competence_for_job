import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include("matrix.urls")),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls)
]

handler500 = "matrix.pages.server_error"
handler404 = "matrix.pages.page_not_found"
handler403csrf = "matrix.pages.csrf_permission_denied"

if settings.DEBUG:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
