import json
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



from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def ver_expediente(request, paciente_id):

    paciente = get_object_or_404(Paciente, id=paciente_id)

    # 🔹 Si no tiene expediente
    if not hasattr(paciente, 'expediente'):
        return render(request, 'expedientes/sin_expediente.html', {
            'paciente': paciente,
            'now': timezone.now()
        })

    expediente = paciente.expediente

    # 🔹 Embarazo activo
    embarazo_activo = expediente.embarazos.filter(activo=True).first()

    # 🔹 Consultas prenatales
    if embarazo_activo:
        consultas_prenatales = ConsultaPrenatal.objects.filter(
            embarazo=embarazo_activo
        ).order_by('-fecha_consulta')
    else:
        consultas_prenatales = ConsultaPrenatal.objects.none()

    context = {
        'paciente': paciente,
        'expediente': expediente,
        'embarazo': embarazo_activo,
        'consultas_prenatales': consultas_prenatales,
        'total_consultas': consultas_prenatales.count(),
        'now': timezone.now(),
    }

      # Obtener embarazo activo
    embarazo = expediente.embarazos.filter(activo=True).first()

    consultas_prenatales = []
    pesos = []
    fechas = []

    if embarazo:
        consultas_prenatales = embarazo.consultas_prenatales.all().order_by('fecha_consulta')

    for consulta in consultas_prenatales:
        pesos.append(float(consulta.peso_madre))
        fechas.append(consulta.fecha_consulta.strftime("%d/%m"))

        context = {
        'expediente': expediente,
        'paciente': expediente.paciente,
        'embarazo': embarazo,
        'consultas_prenatales': consultas_prenatales,
        
        'pesos': json.dumps(pesos),
        'fechas': json.dumps(fechas),
}
                                        

    

    return render(request, 'expedientes/ver_expediente.html', context)

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def expediente_completo(request, paciente_id):

    expediente = get_object_or_404(
        Expediente,
        paciente__id=paciente_id
    )

    embarazos = expediente.embarazos.all().order_by('-creado_en')

    context = {
        'expediente': expediente,
        'paciente': expediente.paciente,
        'embarazos': embarazos,
    }

    return render(
        request,
        'expedientes/expediente_completo.html',
        context
    )

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

        from django.utils.dateparse import parse_datetime

        def checkbox(nombre):
            return nombre in request.POST

        def boolean_select(nombre):
            return request.POST.get(nombre) == "True"

        # convertir fecha
        proxima_cita = parse_datetime(request.POST.get('proxima_cita'))

        # marcar consultas anteriores como atendidas
        ConsultaPrenatal.objects.filter(
            embarazo=embarazo,
            atendida=False
        ).update(atendida=True)

        ConsultaPrenatal.objects.create(

            embarazo=embarazo,
            usuario=request.user,

            # ---------------- GENERALES ----------------
            motivo_consulta=request.POST.get('motivo_consulta'),
            semana_gestacion=request.POST.get('semana_gestacion'),
            calculado_por=request.POST.get('calculado_por'),
            semanas_por_ultrasonido=request.POST.get('semanas_por_ultrasonido') or None,

            # ---------------- SIGNOS VITALES ----------------
            peso_madre=request.POST.get('peso_madre'),
            presion_sistolica=request.POST.get('presion_sistolica'),
            presion_diastolica=request.POST.get('presion_diastolica'),
            frecuencia_cardiaca_materna=request.POST.get('frecuencia_cardiaca_materna') or None,
            frecuencia_respiratoria=request.POST.get('frecuencia_respiratoria') or None,
            temperatura=request.POST.get('temperatura') or None,

            edema=checkbox('edema'),
            proteinuria=checkbox('proteinuria'),

            # ---------------- FETAL ----------------
            altura_uterina=request.POST.get('altura_uterina'),
            frecuencia_cardiaca_fetal=request.POST.get('frecuencia_cardiaca_fetal'),
            movimientos_fetales=boolean_select('movimientos_fetales'),
            presentacion_fetal=request.POST.get('presentacion_fetal'),

            # ---------------- RIESGOS ----------------
            ausencia_movimientos=checkbox('ausencia_movimientos'),
            diabetes_gestacional=checkbox('diabetes_gestacional'),
            hipertension_gestacional=checkbox('hipertension_gestacional'),

            # ---------------- CLINICA ----------------
            sintomas=request.POST.get('sintomas'),
            signos_clinicos=request.POST.get('signos_clinicos'),
            impresion_clinica=request.POST.get('impresion_clinica'),

            # ---------------- CONDUCTA ----------------
            recomendaciones=request.POST.get('recomendaciones'),
            tratamiento=request.POST.get('tratamiento'),

            proxima_cita=proxima_cita,
            atendida=False
        )

        messages.success(request, "Consulta prenatal registrada correctamente")

        return redirect(
            'expedientes:ver_expediente',
            paciente_id=embarazo.expediente.paciente.id
        )


def ganancia_peso(self):
    primera = ConsultaPrenatal.objects.filter(
        embarazo=self.embarazo
    ).order_by('fecha_consulta').first()

    if primera:
        return float(self.peso_madre) - float(primera.peso_madre)
    return 0

def clasificacion_peso(self):
    ganancia = self.ganancia_peso()

    if ganancia < 5:
        return "Ganancia baja"
    elif 5 <= ganancia <= 12:
        return "Ganancia adecuada"
    else:
        return "Ganancia excesiva"  
    

@login_required
def finalizar_embarazo(request, embarazo_id):
    embarazo = get_object_or_404(Embarazo, id=embarazo_id)

    embarazo.activo = False
    embarazo.save()

    messages.success(request, "Embarazo finalizado correctamente.")

    return redirect('expedientes:ver_expediente', embarazo.expediente.paciente.id)

@login_required
def nuevo_embarazo(request, expediente_id):

    expediente = get_object_or_404(Expediente, id=expediente_id)

    # Verificar que no haya embarazo activo
    if expediente.embarazos.filter(activo=True).exists():
        messages.error(request, "Ya existe un embarazo activo.")
        return redirect('expedientes:ver_expediente', expediente.paciente.id)

    Embarazo.objects.create(
        expediente=expediente,
        fecha_ultima_regla=timezone.now().date(),
        activo=True
    )

    messages.success(request, "Nuevo embarazo creado correctamente.")

    return redirect('expedientes:ver_expediente', expediente.paciente.id)


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Embarazo, Expediente


@login_required
def nuevo_embarazo(request, expediente_id):

    expediente = get_object_or_404(Expediente, id=expediente_id)

    if request.method == "POST":
        embarazo = Embarazo.objects.create(
            expediente=expediente,
            fecha_ultima_regla=request.POST.get("fecha_ultima_regla"),
            peso_anterior=request.POST.get("peso_anterior") or None,
            talla=request.POST.get("talla") or None,
            embarazo_planeado=request.POST.get("embarazo_planeado") == "True",
            falla_metodo_anticonceptivo=request.POST.get("falla_metodo") == "True",
            activo=True
        )

        messages.success(request, "Nuevo embarazo registrado correctamente.")
        return redirect("expedientes:ver_expediente", expediente.paciente.id)

    return render(request, "expedientes/nuevo_embarazo.html", {
        "expediente": expediente
    })