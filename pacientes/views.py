# views.py - CORREGIDO
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages  # CORRECCIÓN: Importar messages correctamente
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone  # CORRECCIÓN: Importar timezone correctamente

from django.shortcuts import get_object_or_404, redirect

from NeoVida.settings import LOGOUT_REDIRECT_URL

from .models import Paciente, AntecedentesPersonales, AntecedentesFamiliares, AntecedentesObstetricos

def solo_personal(user):
    return user.is_authenticated and user.rol in ['ADMIN', 'DOCTOR', 'ENFERMERA']

@login_required
@user_passes_test(solo_personal)
def agregar_paciente(request):
    if request.method == 'POST':
        try:
            print(" Procesando formulario...")
            
            # Obtener solo los campos que existen en tu modelo
            nombre = request.POST.get('nombre', '').strip()
            apellido = request.POST.get('apellido', '').strip()
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            edad = request.POST.get('edad', 0)
            
            # Contacto (adaptado a tu modelo)
            telefono = request.POST.get('telefono', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            
            # Demográficos
            estado_civil = request.POST.get('estado_civil', '')
            nivel_educativo = request.POST.get('nivel_educativo', '')
            
            # Validaciones
            if not nombre or not apellido or not fecha_nacimiento:
                messages.error(request, 'Nombre, apellido y fecha de nacimiento son obligatorios')
                return render(request, 'pacientes/agregar_paciente.html', {'request': request})
            
            # Crear paciente con los campos que SÍ existen en tu modelo
            paciente = Paciente.objects.create(
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                edad=int(edad) if edad else 0,
                
                # Adaptar campos a tu modelo actual
                domicilio=direccion,
                telefono=telefono,
                localidad=request.POST.get('municipio', '').strip() or 'No especificado',
                
                estado_civil=estado_civil,
                escolaridad=nivel_educativo,
                
                # Campos adicionales que no están en el formulario pero sí en el modelo
                creado_en=timezone.now(),
                
                # Si necesitas otros campos, agrégalos aquí
                # raza=request.POST.get('raza', '').strip(),
            )
            
            print(f" Paciente creado: {paciente}")
            
            # Crear antecedentes personales (solo campos que existen)
            AntecedentesPersonales.objects.create(
                paciente=paciente,
                diabetes='diabetes' in request.POST,
                hipertension='hipertension' in request.POST,
                tuberculosis='tbc' in request.POST,
                cardiopatia='cardiopatia' in request.POST,
                nefropatia='nefropatia' in request.POST,
                asma='asma' in request.POST,
                vih='vih' in request.POST,
                cirugias_previas=request.POST.get('cirugias', '').strip(),
                otras_enfermedades=request.POST.get('enfermedades_cronicas', '').strip(),
            )
            
            # Crear antecedentes familiares
            AntecedentesFamiliares.objects.create(
                paciente=paciente,
                diabetes='diabetes_familiar' in request.POST,
                hipertension='hipertension_familiar' in request.POST,
                tuberculosis=False,  # No hay en formulario
                cardiopatia='cardiopatias_familiar' in request.POST,
                otras_enfermedades=request.POST.get('otros_antecedentes', '').strip(),
            )
            
            # Crear antecedentes obstétricos
            AntecedentesObstetricos.objects.create(
                paciente=paciente,
                gestas=int(request.POST.get('num_embarazos', 0)),
                partos=int(request.POST.get('num_partos', 0)),
                cesareas=int(request.POST.get('num_cesareas', 0)),
                abortos=int(request.POST.get('num_abortos', 0)),
                nacidos_vivos=int(request.POST.get('num_hijos_vivos', 0)),
                nacidos_muertos=0,  # No hay en formulario
                complicaciones_previas=request.POST.get('complicaciones', '').strip(),
            )
            
            messages.success(request, f' Paciente {nombre} {apellido} creado exitosamente')
            return redirect('panel_principal')   
        except Exception as e:
            print(f" Error: {str(e)}")
            messages.error(request, f'Error al crear paciente: {str(e)}')
            # Para debug, muestra el error completo
            import traceback
            print(traceback.format_exc())
    
    # GET: Mostrar formulario
    return render(request, 'pacientes/agregar_paciente.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Paciente

@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by('-creado_en')
    return render(request, 'pacientes/lista_pacientes.html', {
        'pacientes': pacientes
    })



@login_required
def borrar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    nombre = paciente.nombre_completo

    paciente.delete()  

    messages.success(
        request,
        f"Paciente {nombre} eliminado correctamente (modo pruebas)."
    )

    return redirect('pacientes:lista_pacientes')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Paciente
from expedientes.models import Expediente


@login_required
def panel_paciente(request):
    paciente = get_object_or_404(Paciente, usuario=request.user)
    expediente = paciente.expediente
    embarazo = expediente.embarazos.filter(activo=True).first()

    consultas = []
    proxima_consulta = None

    if embarazo:
        consultas = embarazo.consultas_prenatales.order_by('-fecha_consulta')
        proxima_consulta = consultas.filter(atendida=False).order_by('proxima_cita').first()

    return render(request, 'pacientes/panel_paciente.html', {
        'paciente': paciente,
        'embarazo': embarazo,
        'consultas': consultas,
        'proxima_consulta': proxima_consulta
    })

def logout_view(request):
    LOGOUT_REDIRECT_URL(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')  # Redirige a la página de login