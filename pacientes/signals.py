from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from usuarios.models import Usuario
from .models import Paciente
import random
import string


def generar_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


@receiver(post_save, sender=Paciente)
def crear_usuario_paciente(sender, instance, created, **kwargs):
    if created and instance.usuario is None:
        username = slugify(f"{instance.nombre}.{instance.apellido}")[:20]
        password = generar_password()

        usuario = Usuario.objects.create_user(
            username=username,
            password=password,
            rol='PACIENTE'
        )

        instance.usuario = usuario
        instance.save()

        # SOLO PARA DESARROLLO / PRUEBAS
        print("Usuario creado automáticamente")
        print("Username:", username)
        print("Password:", password)


from expedientes.models import Expediente
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Paciente


@receiver(post_save, sender=Paciente)
def crear_expediente_paciente(sender, instance, created, **kwargs):
    """
    Al crear una paciente, se crea automáticamente su expediente clínico.
    """
    if created:
        Expediente.objects.create(
            paciente=instance
        )
