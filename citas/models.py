from django.db import models
from expedientes.models import Embarazo
from usuarios.models import Usuario


class Cita(models.Model):
    embarazo = models.ForeignKey(
        Embarazo,
        on_delete=models.CASCADE,
        related_name='citas'
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        help_text="Profesional que agenda la cita"
    )

    fecha = models.DateTimeField(
        help_text="Fecha y hora de la cita"
    )

    atendida = models.BooleanField(
        default=False,
        help_text="Indica si la cita ya fue atendida"
    )

    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita {self.fecha}"
