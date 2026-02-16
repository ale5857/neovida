from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'activo', 'is_staff')
    list_filter = ('rol', 'activo')
    search_fields = ('username', 'email')
