from collections import UserDict
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .forms import CrearUsuarioForm
from .models import Usuario

# ===============================
# LOGIN
# ===============================
class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.rol == 'PACIENTE':
            return redirect('pacientes:panel_paciente').url

        if user.rol in ['ADMIN', 'DOCTOR', 'ENFERMERA']:
            return redirect('pacientes:lista_pacientes').url

        # fallback de seguridad
        return '/'



# ===============================
# PERMISOS
# ===============================
def es_admin(user):
    return user.is_authenticated and user.rol == 'ADMIN'

# ===============================
# CREAR USUARIO
# ===============================
@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            
            # Generar contraseña automática
            password_generada = form.generar_password()
            usuario.set_password(password_generada)
            usuario.save()
            
            # Preparar resumen
            resumen_usuario = {
                'username': usuario.username,
                'rol': usuario.rol,
                'rol_display': usuario.get_rol_display(),
                'password': password_generada,
                'email': usuario.email,
                'nombre_completo': f"{usuario.first_name} {usuario.last_name}",
                'fecha_creacion': usuario.date_joined.strftime("%d/%m/%Y %H:%M"),
            }
            
            # Mostrar formulario vacío con modal de resumen
            return render(request, 'usuarios/crear_usuario.html', {
                'form': CrearUsuarioForm(),
                'resumen_usuario': resumen_usuario,
                'mostrar_resumen': True
            })
    else:
        form = CrearUsuarioForm()
    
    return render(request, 'usuarios/crear_usuario.html', {'form': form})
# ===============================
# LISTA DE USUARIOS (SOLO ADMIN)
# ===============================
@login_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all()

    resumen = request.session.pop('usuario_creado_resumen', None)

    return render(request, 'usuarios/lista_usuarios.html', {
        'usuarios': usuarios,
        'resumen_usuario': resumen
    })

# ===============================
# ACTIVAR / DESACTIVAR USUARIO
# ===============================
@login_required
@user_passes_test(es_admin)
def toggle_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    # 🔒 Evitar que el admin se desactive a sí mismo
    if usuario == request.user:
        return redirect('usuarios:lista_usuarios')

    usuario.is_active = not usuario.is_active
    usuario.save()

    return redirect('usuarios:lista_usuarios')


# ===============================
# EDITAR USUARIO (MODAL)
# ===============================
@login_required
@user_passes_test(es_admin)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username:
            usuario.username = username

        # Cambiar contraseña solo si se escribe una nueva
        if password:
            usuario.set_password(password)

        usuario.save()
        return JsonResponse({'success': True})

    # GET → datos para llenar el modal
    return JsonResponse({
        'username': usuario.username,
        'rol': usuario.rol
    })

from django.views.decorators.http import require_POST

@login_required
@user_passes_test(es_admin)
@require_POST
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    # Evitar que el admin se elimine a sí mismo
    if usuario == request.user:
        return JsonResponse({
            'success': False,
            'error': 'No puedes eliminar tu propia cuenta'
        }, status=400)

    usuario.delete()
    return JsonResponse({'success': True})


from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        user = self.request.user

        if user.rol == 'PACIENTE':
            return redirect('pacientes:panel_paciente').url

        if user.rol in ['ADMIN', 'DOCTOR', 'ENFERMERA']:
            return redirect('pacientes:lista_pacientes').url

        return '/'
