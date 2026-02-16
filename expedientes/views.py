from time import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from citas.models import Cita
from .models import Expediente, Embarazo
from pacientes.models import Paciente
from consultas.models import ConsultaPrenatal  # Importar el modelo de consultas

from django.utils import timezone
from datetime import datetime



@login_required
def ver_expediente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if not hasattr(paciente, 'expediente'):
        return render(request, 'expedientes/sin_expediente.html', {
            'paciente': paciente,
            'expediente': expediente,
            'now': timezone.now()
        })
    
    

    expediente = paciente.expediente
    embarazo_activo = expediente.embarazos.filter(activo=True).first()
    
    # OBTENER CONSULTAS PRENATALES
    consultas_prenatales = []
    if embarazo_activo:
        consultas_prenatales = ConsultaPrenatal.objects.filter(
            embarazo=embarazo_activo
        ).order_by('-fecha_consulta')  # Más recientes primero

    return render(request, 'expedientes/ver_expediente.html', {
        'paciente': paciente,
        'expediente': expediente,
        'embarazo': embarazo_activo,
        'consultas_prenatales': consultas_prenatales,  # ¡IMPORTANTE!
        'total_consultas': consultas_prenatales.count(),
    })
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def expediente_completo(request, paciente_id):
    expediente = get_object_or_404(Expediente, paciente_id=paciente_id)


    if request.user.rol not in ['DOCTOR', 'ENFERMERA', 'ADMIN']:
        return HttpResponseForbidden("No tienes permiso para ver este expediente")

    expediente = get_object_or_404(Expediente, id=expediente)
    embarazo_activo = expediente.embarazos.filter(activo=True).first()

    context = {
        'expediente': expediente,
        'paciente': expediente.paciente,
        'embarazo': embarazo_activo,
        'consultas': embarazo_activo.consultas.all() if embarazo_activo else [],
        'vacunas': embarazo_activo.vacunas.all() if embarazo_activo else [],
        'laboratorios': embarazo_activo.laboratorios.all() if embarazo_activo else [],
        'ultrasonidos': embarazo_activo.ultrasonidos.all() if embarazo_activo else [],
    }

    return render(request, 'expedientes/expediente_completo.html', context)


from consultas.models import ConsultaPrenatal
from expedientes.models import Embarazo


@login_required
def crear_consulta_prenatal(request, expediente_id):
    embarazo = get_object_or_404(
        Embarazo,
        expediente_id=expediente_id,
        activo=True
    )

    if request.method == 'POST':

        campos_obligatorios = [
            'semana_gestacion', 'peso_madre',
            'presion_sistolica', 'presion_diastolica',
            'altura_uterina', 'frecuencia_cardiaca_fetal',
            'sintomas', 'signos_alarma',
            'impresion_clinica', 'recomendaciones',
            'tratamiento', 'proxima_cita'
        ]

        for campo in campos_obligatorios:
            if not request.POST.get(campo):
                messages.error(
                    request,
                    "Todos los campos clínicos son obligatorios."
                )
                return redirect(
                    'expedientes:ver_expediente',
                    paciente_id=embarazo.expediente.paciente.id
                )

        # 🔴 🔴 🔴 AQUÍ ESTÁ LA LÓGICA CLAVE 🔴 🔴 🔴
        # Marcar como ATENDIDAS todas las consultas anteriores del embarazo
        ConsultaPrenatal.objects.filter(
            embarazo=embarazo,
            atendida=False
        ).update(atendida=True)

        # ✅ Crear la nueva consulta (queda PENDIENTE)
        ConsultaPrenatal.objects.create(
            embarazo=embarazo,
            usuario=request.user,
            semana_gestacion=request.POST['semana_gestacion'],
            peso_madre=request.POST['peso_madre'],
            presion_sistolica=request.POST['presion_sistolica'],
            presion_diastolica=request.POST['presion_diastolica'],
            edema=bool(request.POST.get('edema')),
            proteinuria=bool(request.POST.get('proteinuria')),
            altura_uterina=request.POST['altura_uterina'],
            frecuencia_cardiaca_fetal=request.POST['frecuencia_cardiaca_fetal'],
            movimientos_fetales=bool(request.POST.get('movimientos_fetales')),
            sintomas=request.POST['sintomas'],
            signos_alarma=request.POST['signos_alarma'],
            impresion_clinica=request.POST['impresion_clinica'],
            recomendaciones=request.POST['recomendaciones'],
            tratamiento=request.POST['tratamiento'],
            proxima_cita=request.POST['proxima_cita'],
            atendida=False  # explícito para claridad
        )

        messages.success(
            request,
            "Consulta prenatal registrada correctamente."
        )

        return redirect(
            'expedientes:ver_expediente',
            paciente_id=embarazo.expediente.paciente.id
        )