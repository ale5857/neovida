from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from usuarios.models import Usuario
from pacientes.models import Paciente
from expedientes.models import Embarazo
from consultas.models import ConsultaPrenatal


@login_required
def panel_principal(request):
    rol = request.user.rol.upper()
    hoy = timezone.now().date()
    fin_semana = hoy + timedelta(days=6)

    # =========================
    # PANEL ADMIN
    # =========================
    if rol == 'ADMIN':
        context = {
            'total_usuarios': Usuario.objects.count(),
            'total_doctores': Usuario.objects.filter(rol='DOCTOR').count(),
            'total_enfermeras': Usuario.objects.filter(rol='ENFERMERA').count(),
            'total_pacientes': Paciente.objects.count(),
        }
        template = 'dashboard/admin.html'

    # =========================
    # PANEL DOCTOR
    # =========================
    elif rol == 'DOCTOR':

        consultas = ConsultaPrenatal.objects.filter(
            usuario=request.user,
            proxima_cita__range=(hoy, fin_semana)
        ).select_related(
            'embarazo',   # ✅ existe
            'usuario'     # ✅ existe
        ).order_by('proxima_cita')

        citas_hoy = consultas.filter(proxima_cita=hoy)

        pacientes = Paciente.objects.filter(
            expediente__embarazos__consultas_prenatales__usuario=request.user
        ).distinct()

        context = {
            'citas_hoy': citas_hoy,
            'agenda_semanal': consultas,
            'total_pacientes': pacientes.count(),
            'alertas': consultas.count(),
        }

        template = 'dashboard/doctor.html'

    # =========================
    # PANEL ENFERMERA
    # =========================
    elif rol == 'ENFERMERA':

        citas_hoy = ConsultaPrenatal.objects.filter(
            proxima_cita=hoy
        ).select_related(
            'embarazo',
            'usuario'
        )

        agenda_semanal = ConsultaPrenatal.objects.filter(
            proxima_cita__range=(hoy, fin_semana)
        ).select_related(
            'embarazo',
            'usuario'
        ).order_by('proxima_cita')

        pacientes = Paciente.objects.filter(
            expediente__embarazos__consultas_prenatales__in=agenda_semanal
        ).distinct()

        context = {
            'citas_hoy': citas_hoy,
            'agenda_semanal': agenda_semanal,
            'total_pacientes': pacientes.count(),
        }

        template = 'dashboard/enfermera.html'

    # =========================
    # PANEL PACIENTE
    # =========================
    elif rol == 'PACIENTE':
        paciente = getattr(request.user, 'paciente', None)

        embarazo = Embarazo.objects.filter(
            expediente__paciente=paciente,
            activo=True
        ).first() if paciente else None

        consultas = ConsultaPrenatal.objects.filter(
            embarazo__expediente__paciente=paciente
        ).order_by('-fecha_consulta')[:5]

        context = {
            'paciente': paciente,
            'embarazo': embarazo,
            'consultas': consultas,
        }

        template = 'pacientes/panel_paciente.html'

    else:
        context = {}
        template = 'dashboard/dashboard_base.html'

    return render(request, template, context)
