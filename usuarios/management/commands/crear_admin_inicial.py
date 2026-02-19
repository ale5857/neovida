from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Crea el administrador inicial si no existe'

    def handle(self, *args, **kwargs):

        if not Usuario.objects.filter(username='admin').exists():

            Usuario.objects.create_superuser(
                username='admin',
                email='admin@neovida.com',
                password='1234*',
                rol='ADMIN'
            )

            self.stdout.write(self.style.SUCCESS('✔ Admin inicial creado'))
        else:
            self.stdout.write(self.style.WARNING('El admin ya existe'))