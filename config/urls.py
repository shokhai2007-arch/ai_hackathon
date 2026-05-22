from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.urls')),
    path('', serve, {'path': 'landing_paage.html', 'document_root': settings.STATICFILES_DIRS[0]}),
    re_path(r'^landing/?$', serve, {'path': 'landing_paage.html', 'document_root': settings.STATICFILES_DIRS[0]}),
    re_path(r'^(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
]
