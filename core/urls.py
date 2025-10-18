"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("users.urls", namespace='user')),
    path('blog/', include("blog.urls", namespace='blog')),
    path('short/', include("short.urls", namespace='short')),
    path('chat/', include("chat.urls", namespace='chat')),
    path('froala_editor/', include('froala_editor.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


