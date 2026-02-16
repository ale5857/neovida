from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from consultas.models import ConsultaPrenatal


@login_required
def agenda_citas(request):
    now = timezone.now()

    citas = ConsultaPrenatal.objects.select_related(
        'embarazo__expediente__paciente',
        'usuario'
    ).filter(
        proxima_cita__gte=now
    ).order_by('proxima_cita')

    return render(request, 'citas/agenda.html', {
        'citas': citas,
        'now': now,
        'today': now.date()
    })
