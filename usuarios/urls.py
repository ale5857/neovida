from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import UsuarioLoginView, crear_usuario

app_name = 'usuarios'   # 👈 ESTO ES OBLIGATORIO

urlpatterns = [
    path('', UsuarioLoginView.as_view(), name='login'),
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('crear/', crear_usuario, name='crear_usuario'),
    path('editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),


    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('toggle/<int:user_id>/', views.toggle_usuario, name='toggle_usuario'),


]
