from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario del sistema NeoVida.
    Roles: Administrador, Doctor, Enfermera
    """

    ROLES = (
        ('ADMIN', 'Administrador'),
        ('DOCTOR', 'Doctor'),
        ('ENFERMERA', 'Enfermera'),
        ('PACIENTE', 'Paciente'),
    )

    rol = models.CharField(max_length=20, choices=ROLES)
    activo = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"
    
    def get_rol_display(self):
        """Devuelve el nombre legible del rol"""
        return dict(self.ROLES).get(self.rol, self.rol)