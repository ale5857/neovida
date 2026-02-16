from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from consultas.models import ConsultaPrenatal


@login_required
def detalle_consulta(request, consulta_id):
    consulta = get_object_or_404(ConsultaPrenatal, id=consulta_id)

    return render(request, 'consultas/detalle_consulta.html', {
        'consulta': consulta
    })
