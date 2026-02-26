# ===============================
# IMPORTS
# ===============================

import uuid
import random
from django.utils.text import slugify
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.forms import ValidationError
from django.http import JsonResponse

from usuarios.models import Usuario
from .models import (
    Paciente,
    AntecedentesPersonales,
    AntecedentesFamiliares,
    AntecedentesObstetricos
)

from expedientes.models import Expediente


# ===============================
# UTILIDADES
# ===============================

def solo_personal(user):
    return user.is_authenticated and user.rol in ['ADMIN', 'DOCTOR', 'ENFERMERA']


def generar_password(longitud=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))


def calcular_riesgo(paciente):
    """
    Clasificación simple tipo MINSA
    """
    try:
        ap = paciente.antecedentes_personales

        if ap.diabetes or ap.hipertension or ap.preeclampsia or ap.eclampsia:
            return "Alto"

        if ap.asma or ap.cardiopatia or ap.nefropatia:
            return "Medio"

    except:
        pass

    return "Bajo"


# ===============================
# CREAR PACIENTE
# ===============================
@login_required
@user_passes_test(solo_personal)
def agregar_paciente(request):

    if request.method == 'POST':

        try:
            with transaction.atomic():

                # ===== DATOS PRINCIPALES =====
                nombre = request.POST.get('nombre', '').strip()
                apellido = request.POST.get('apellido', '').strip()
                fecha_nacimiento = request.POST.get('fecha_nacimiento')
                telefono = request.POST.get('telefono', '').strip()
                direccion = request.POST.get('direccion', '').strip()
                municipio = request.POST.get('municipio', '').strip()
                estado_civil = request.POST.get('estado_civil', '')
                nivel_educativo = request.POST.get('nivel_educativo', '')

                if not nombre or not apellido or not fecha_nacimiento:
                    messages.error(
                        request,
                        "Nombre, apellido y fecha de nacimiento son obligatorios."
                    )
                    return render(request, 'pacientes/agregar_paciente.html')

                # ===== GENERAR PASSWORD =====
                password_generado = generar_password()

                # ===== GENERAR USERNAME CON NOMBRE =====
                base_username = slugify(f"{nombre}.{apellido}")
                base_username = base_username.replace("-", "")

                username = base_username

                while Usuario.objects.filter(username=username).exists():
                    username = f"{base_username}{random.randint(10,99)}"

                # ===== CREAR USUARIO =====
                usuario = Usuario.objects.create(
                    username=username,
                    email=f"{uuid.uuid4().hex[:10]}@paciente.local",
                    rol="PACIENTE"
                )

                usuario.set_password(password_generado)
                usuario.save()

                # ===== CREAR PACIENTE =====
                paciente = Paciente.objects.create(
                    usuario=usuario,
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=fecha_nacimiento,
                    domicilio=direccion,
                    localidad=municipio or "No especificado",
                    telefono=telefono,
                    estado_civil=estado_civil,
                    escolaridad=nivel_educativo,
                )

                # ===== ANTECEDENTES PERSONALES =====
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

                # ===== ANTECEDENTES FAMILIARES =====
                AntecedentesFamiliares.objects.create(
                    paciente=paciente,
                    diabetes='diabetes_familiar' in request.POST,
                    hipertension='hipertension_familiar' in request.POST,
                    cardiopatia='cardiopatias_familiar' in request.POST,
                    otras_enfermedades=request.POST.get('otros_antecedentes', '').strip(),
                )

                # ===== ANTECEDENTES OBSTETRICOS =====
                AntecedentesObstetricos.objects.create(
                    paciente=paciente,
                    gestas=int(request.POST.get('num_embarazos', 0)),
                    partos=int(request.POST.get('num_partos', 0)),
                    cesareas=int(request.POST.get('num_cesareas', 0)),
                    abortos=int(request.POST.get('num_abortos', 0)),
                    nacidos_vivos=int(request.POST.get('num_hijos_vivos', 0)),
                    complicaciones_previas=request.POST.get('complicaciones', '').strip(),
                )

                # ===== MOSTRAR RESUMEN =====
                return render(request, "pacientes/resumen_creacion.html", {
                    "paciente": paciente,
                    "username": usuario.username,
                    "password": password_generado
                })

        except ValidationError as e:
            messages.error(request, e.messages)

        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")

    return render(request, 'pacientes/agregar_paciente.html')

# ===============================
# LISTA DE PACIENTES
# ===============================

@login_required
def lista_pacientes(request):
    return render(request, 'pacientes/lista_pacientes.html')


@login_required
def api_pacientes(request):

    search = request.GET.get("search", "")
    filtro = request.GET.get("filter", "todos")
    page = request.GET.get("page", 1)

    pacientes = Paciente.objects.all().order_by("-id")

    if search:
        pacientes = pacientes.filter(
            Q(nombre__icontains=search) |
            Q(apellido__icontains=search) |
            Q(telefono__icontains=search)
        )

    paginator = Paginator(pacientes, 6)
    page_obj = paginator.get_page(page)

    data = []

    for p in page_obj:

        riesgo = calcular_riesgo(p)

        if filtro == "alto" and riesgo != "Alto":
            continue

        try:
            ao = p.antecedentes_obstetricos
            gestas = ao.gestas
            partos = ao.partos
            abortos = ao.abortos
        except:
            gestas = partos = abortos = 0

        enfermedades = []
        try:
            ap = p.antecedentes_personales
            if ap.diabetes: enfermedades.append("Diabetes")
            if ap.hipertension: enfermedades.append("Hipertensión")
            if ap.preeclampsia: enfermedades.append("Preeclampsia")
            if ap.eclampsia: enfermedades.append("Eclampsia")
            if ap.cardiopatia: enfermedades.append("Cardiopatía")
            if ap.nefropatia: enfermedades.append("Nefropatía")
        except:
            pass

        data.append({
            "id": p.id,
            "nombre": p.nombre_completo,
            "edad": p.edad,
            "telefono": p.telefono,
            "direccion": p.domicilio,
            "localidad": p.localidad,
            "estado_civil": p.estado_civil,
            "escolaridad": p.escolaridad,
            "gestas": gestas,
            "partos": partos,
            "abortos": abortos,
            "riesgo": riesgo,
            "enfermedades": enfermedades,
            "embarazo_activo": True
        })

    return JsonResponse({
        "pacientes": data,
        "has_next": page_obj.has_next()
    })


# ===============================
# BORRAR PACIENTE
# ===============================

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


# ===============================
# PANEL PACIENTE
# ===============================

@login_required
def panel_paciente(request):

    paciente = get_object_or_404(Paciente, usuario=request.user)
    expediente = paciente.expediente
    embarazo = expediente.embarazos.filter(activo=True).first()

    consultas = []
    proxima_consulta = None

    if embarazo:
        consultas = embarazo.consultas_prenatales.order_by('-fecha_consulta')
        proxima_consulta = consultas.filter(
            atendida=False
        ).order_by('proxima_cita').first()

    return render(request, 'pacientes/panel_paciente.html', {
        'paciente': paciente,
        'embarazo': embarazo,
        'consultas': consultas,
        'proxima_consulta': proxima_consulta
    })


# ===============================
# LOGOUT
# ===============================

def logout_view(request):
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')