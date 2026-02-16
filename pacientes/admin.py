from django.contrib import admin
from .models import (
    Paciente,
    AntecedentesPersonales,
    AntecedentesFamiliares,
    AntecedentesObstetricos
)


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'edad', 'telefono')
    search_fields = ('nombre', 'apellido', 'telefono')


admin.site.register(AntecedentesPersonales)
admin.site.register(AntecedentesFamiliares)
admin.site.register(AntecedentesObstetricos)
