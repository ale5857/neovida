from django.contrib import admin
from .models import ConsultaPrenatal


@admin.register(ConsultaPrenatal)
class ConsultaPrenatalAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_consulta',
        'embarazo',
        'usuario',
        'semana_gestacion',
        'presion_sistolica',
        'presion_diastolica',
    )

    list_filter = (
        'fecha_consulta',
        'usuario',
        'semana_gestacion',
        'edema',
        'proteinuria',
    )

    search_fields = (
        'embarazo__expediente__paciente__nombre',
        'embarazo__expediente__paciente__apellido',
    )
