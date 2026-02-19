from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views
from .views import UsuarioLoginView, crear_usuario
from .tokens import password_reset_token   # 👈 IMPORTANTE

app_name = 'usuarios'

urlpatterns = [

    # =========================
    # LOGIN / LOGOUT
    # =========================
    path('', UsuarioLoginView.as_view(), name='login'),
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='usuarios:login'), name='logout'),

    # =========================
    # USUARIOS
    # =========================
    path('crear/', crear_usuario, name='crear_usuario'),
    path('editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('toggle/<int:user_id>/', views.toggle_usuario, name='toggle_usuario'),

    # =========================
    # RECUPERAR CONTRASEÑA
    # =========================

    # pedir correo
    path('password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('usuarios:password_reset_done')
        ),
        name='password_reset'),

    # correo enviado
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'),

    # 👉 AQUI ESTA EL CAMBIO IMPORTANTE
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            token_generator=password_reset_token   # 🔥 SOLUCION
        ),
        name='password_reset_confirm'),

    # contraseña cambiada
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'),
]