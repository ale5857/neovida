from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    email = models.EmailField(
        'correo electrónico',
        unique=True,
        blank=False,
        null=False
    )

    ROLES = (
        ('ADMIN', 'Administrador'),
        ('DOCTOR', 'Doctor'),
        ('ENFERMERA', 'Enfermera'),
        ('PACIENTE', 'Paciente'),
    )

    rol = models.CharField(max_length=20, choices=ROLES)
    activo = models.BooleanField(default=True)  # tu control interno

    def __str__(self):
        return f"{self.username} ({self.rol})"
    
    def get_rol_display(self):
        return dict(self.ROLES).get(self.rol, self.rol)