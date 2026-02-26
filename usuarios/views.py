from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import CrearUsuarioForm
from .models import Usuario


# =====================================================
# LOGIN
# =====================================================
class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos")
        return super().form_invalid(form)

    
    def get_success_url(self):
        user = self.request.user

        if user.rol == 'PACIENTE':
             return reverse_lazy('pacientes:panel_paciente')

        elif user.rol in ['DOCTOR', 'ENFERMERA', 'ADMIN']:
             return reverse_lazy('panel_principal')

          # fallback seguro
        return reverse_lazy('panel_principal')


# =====================================================
# PERMISOS
# =====================================================
def es_admin(user):
    return user.is_authenticated and user.rol == 'ADMIN'


# =====================================================
# CREAR USUARIO
# =====================================================
@login_required
@user_passes_test(es_admin)
def crear_usuario(request):

    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)

            password_generada = form.generar_password()
            usuario.set_password(password_generada)
            usuario.save()

            resumen_usuario = {
                'username': usuario.username,
                'rol': usuario.rol,
                'rol_display': usuario.get_rol_display(),
                'password': password_generada,
                'email': usuario.email,
                'nombre_completo': f"{usuario.first_name} {usuario.last_name}",
                'fecha_creacion': usuario.date_joined.strftime("%d/%m/%Y %H:%M"),
            }

            return render(request, 'usuarios/crear_usuario.html', {
                'form': CrearUsuarioForm(),
                'resumen_usuario': resumen_usuario,
                'mostrar_resumen': True
            })

    else:
        form = CrearUsuarioForm()

    return render(request, 'usuarios/crear_usuario.html', {'form': form})


# =====================================================
# LISTA USUARIOS
# =====================================================
@login_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    resumen = request.session.pop('usuario_creado_resumen', None)

    return render(request, 'usuarios/lista_usuarios.html', {
        'usuarios': usuarios,
        'resumen_usuario': resumen
    })


# =====================================================
# ACTIVAR / DESACTIVAR
# =====================================================
@login_required
@user_passes_test(es_admin)
def toggle_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    if usuario == request.user:
        return redirect('usuarios:lista_usuarios')

    usuario.is_active = not usuario.is_active
    usuario.save()

    return redirect('usuarios:lista_usuarios')


# =====================================================
# EDITAR USUARIO
# =====================================================
@login_required
@user_passes_test(es_admin)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    if request.method == 'POST':

        # 🚫 bloquear si intenta editarse
        if usuario == request.user:
            return JsonResponse({
                'success': False,
                'error': 'No puedes modificar tu propia cuenta desde aquí'
            }, status=403)

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        rol = request.POST.get('rol')
        password = request.POST.get('password')

        if username:
            usuario.username = username
        if first_name:
            usuario.first_name = first_name
        if last_name:
            usuario.last_name = last_name
        if rol:
            usuario.rol = rol
        if password:
            usuario.set_password(password)

        usuario.save()
        return JsonResponse({'success': True})

    return JsonResponse({
        'username': usuario.username,
        'first_name': usuario.first_name,
        'last_name': usuario.last_name,
        'rol': usuario.rol
    })
# =====================================================
# ELIMINAR USUARIO
# =====================================================
@login_required
@user_passes_test(es_admin)
@require_POST
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    if usuario == request.user:
        return JsonResponse({
            'success': False,
            'error': 'No puedes eliminar tu propia cuenta'
        }, status=400)

    usuario.delete()
    return JsonResponse({'success': True})