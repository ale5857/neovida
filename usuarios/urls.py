from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views
from .views import UsuarioLoginView, crear_usuario

app_name = 'usuarios'

urlpatterns = [
    # LOGIN / LOGOUT
    path('', UsuarioLoginView.as_view(), name='login'),
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='usuarios:login'), name='logout'),

    # USUARIOS
    path('crear/', crear_usuario, name='crear_usuario'),
    path('editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('toggle/<int:user_id>/', views.toggle_usuario, name='toggle_usuario'),

    # =========================
    # RECUPERAR CONTRASEÑA
    # =========================
    path('recuperar/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/password_reset_form.html'
    ), name='password_reset'),

    path('recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuarios/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='usuarios/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='usuarios/password_reset_complete.html'
    ), name='password_reset_complete'),
]
