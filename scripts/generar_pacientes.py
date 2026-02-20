import random
from pacientes.models import Paciente
from django.utils import timezone

nombres = ["Maria","Juana","Ana","Rosa","Lucia","Carmen","Elena","Paola","Andrea","Laura"]
apellidos = ["Lopez","Martinez","Perez","Gomez","Hernandez","Diaz","Torres","Ramirez"]
import random
from datetime import date, timedelta
from django.utils import timezone
from pacientes.models import Paciente

nombres = ["Maria","Juana","Ana","Rosa","Lucia","Carmen","Elena","Paola","Andrea","Laura"]
apellidos = ["Lopez","Martinez","Perez","Gomez","Hernandez","Diaz","Torres","Ramirez"]

for i in range(500):

    edad = random.randint(15,40)
    nacimiento = date.today() - timedelta(days=edad*365)

    Paciente.objects.create(
        nombre=random.choice(nombres),
        apellido=random.choice(apellidos),
        fecha_nacimiento=nacimiento,
        edad=edad,
        telefono=f"8888{random.randint(1000,9999)}",
        domicilio="Barrio Central",
        localidad="Managua",
        raza="Mestiza",
        estado_civil=random.choice(["Soltera","Acompañada","Casada"]),
        escolaridad=random.choice(["Primaria","Secundaria","Universidad"]),
        creado_en=timezone.now()
    )

print("500 pacientes creados ✔")