from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .models import Expediente, Embarazo


@receiver(post_save, sender=Expediente)
def crear_embarazo_inicial(sender, instance, created, **kwargs):
    """
    Al crear un expediente, se crea automáticamente un embarazo activo.
    """
    if created:
        Embarazo.objects.create(
            expediente=instance,
            fecha_ultima_regla=date.today(),
            semanas_gestacion=0,
            activo=True
        )
