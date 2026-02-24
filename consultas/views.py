from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from consultas.models import ConsultaPrenatal


@login_required
def detalle_consulta(request, consulta_id):
    consulta = get_object_or_404(ConsultaPrenatal, id=consulta_id)

    consulta_anterior = ConsultaPrenatal.objects.filter(
        embarazo=consulta.embarazo,
        fecha_consulta__lt=consulta.fecha_consulta
    ).order_by('-fecha_consulta').first()

    diferencia_peso = None
    diferencia_presion = None

    if consulta_anterior:
        diferencia_peso = float(consulta.peso_madre) - float(consulta_anterior.peso_madre)
        diferencia_presion = (
            consulta.presion_sistolica - consulta_anterior.presion_sistolica,
            consulta.presion_diastolica - consulta_anterior.presion_diastolica
        )

    return render(request, 'consultas/detalle_consulta.html', {
        'consulta': consulta,
        'consulta_anterior': consulta_anterior,
        'diferencia_peso': diferencia_peso,
        'diferencia_presion': diferencia_presion,
    })