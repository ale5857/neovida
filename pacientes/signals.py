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

        base_username = slugify(f"{instance.nombre}.{instance.apellido}")[:20]
        username = base_username
        contador = 1

        # asegurar username único
        while Usuario.objects.filter(username=username).exists():
            username = f"{base_username}{contador}"[:20]
            contador += 1

        password = generar_password()

        # email único real
        email = f"{username}@paciente.local"

        # 🔥 crear usuario manualmente (no create_user)
        usuario = Usuario(
            username=username,
            email=email,
            rol='PACIENTE'
        )

        usuario.set_password(password)
        usuario.save()

        instance.usuario = usuario
        instance.save(update_fields=["usuario"])
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
