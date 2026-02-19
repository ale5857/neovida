from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Raíz → Login
    path('', lambda request: redirect('usuarios:login')),

    # Apps
    path('usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('dashboard/', include('dashboard.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('expedientes/', include('expedientes.urls')),
    path('consultas/', include('consultas.urls')),
    path('citas/', include('citas.urls')),
    # Admin
    path('admin/', admin.site.urls),
]

# STATIC + MEDIA EN DESARROLLO
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                