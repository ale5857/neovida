from django.contrib import admin
from .models import Expediente, Embarazo, Vacuna


@admin.register(Expediente)
class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'fecha_apertura', 'estado')
    search_fields = ('paciente__nombre', 'paciente__apellido')
    list_filter = ('estado',)


@admin.register(Embarazo)
class EmbarazoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'expediente',
        'mostrar_semanas',
        'activo',
        'creado_en'
    )

    list_filter = ('activo',)

    def mostrar_semanas(self, obj):
        return obj.semanas_gestacion

    mostrar_semanas.short_description = "Semanas"


@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'embarazo',
        'fecha_aplicacion',
        'dosis'
    )
    list_filter = ('nombre', 'fecha_aplicacion')
    search_fields = (
        'nombre',
        'embarazo__expediente__paciente__nombre',
        'embarazo__expediente__paciente__apellido',
    )


from .models import Laboratorio


@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = (
        'fecha',
        'embarazo',
        'hb_menor_20_sem',
        'hb_mayor_20_sem',
        'vih',
        'sifilis'
    )
    list_filter = ('fecha', 'vih', 'sifilis')
    search_fields = (
        'embarazo__expediente__paciente__nombre',
        'embarazo__expediente__paciente__apellido',
    )

from .models import Ultrasonido


@admin.register(Ultrasonido)
class UltrasonidoAdmin(admin.ModelAdmin):
    list_display = (
        'fecha',
        'embarazo',
        'semanas_gestacion',
        'peso_estimado'
    )
    list_filter = ('fecha',)
    search_fields = (
        'embarazo__expediente__paciente__nombre',
        'embarazo__expediente__paciente__apellido',
    )
