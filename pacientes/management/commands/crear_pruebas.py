from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date
import random
import string
import uuid

from usuarios.models import Usuario
from pacientes.models import (
    Paciente,
    AntecedentesPersonales,
    AntecedentesFamiliares,
    AntecedentesObstetricos
)


class Command(BaseCommand):
    help = "Crea pacientes completos de prueba con usuarios y antecedentes"

    def generar_password(self, longitud=8):
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(longitud))

    def generar_telefono_unico(self):
        while True:
            telefono = f"88{random.randint(100000, 999999)}"
            if not Usuario.objects.filter(username=telefono).exists():
                return telefono

    def handle(self, *args, **kwargs):

        cantidad = 20

        for i in range(1, cantidad + 1):

            try:
                with transaction.atomic():

                    # ================= TELEFONO ÚNICO =================
                    telefono = self.generar_telefono_unico()
                    password = self.generar_password()

                    # ================= CREAR USUARIO =================
                    usuario = Usuario(
                        username=telefono,
                        email=f"{uuid.uuid4().hex[:12]}@paciente.local",
                        rol="PACIENTE"
                    )

                    usuario.set_password(password)
                    usuario.save()

                    # ================= CREAR PACIENTE =================
                    paciente = Paciente(
                        usuario=usuario,
                        nombre=f"Paciente{i}",
                        apellido="Prueba",
                        fecha_nacimiento=date(
                            random.randint(1980, 2005),
                            random.randint(1, 12),
                            random.randint(1, 28)
                        ),
                        domicilio="Barrio Centro",
                        localidad="Managua",
                        telefono=telefono,
                        estado_civil=random.choice(["Soltera", "Casada"]),
                        escolaridad=random.choice(["Primaria", "Secundaria", "Universitaria"])
                    )

                    paciente.full_clean()
                    paciente.save()

                    # ================= ANTECEDENTES PERSONALES =================
                    riesgo_alto = random.choice([True, False])

                    antecedentes_personales = AntecedentesPersonales(
                        paciente=paciente,
                        diabetes=riesgo_alto,
                        hipertension=riesgo_alto,
                        asma=random.choice([True, False]),
                        cardiopatia=random.choice([True, False]),
                        vih=random.choice([True, False]),
                        sifilis=random.choice([True, False]),
                        preeclampsia=random.choice([True, False]),
                        eclampsia=random.choice([True, False]),
                    )

                    antecedentes_personales.full_clean()
                    antecedentes_personales.save()

                    # ================= ANTECEDENTES FAMILIARES =================
                    AntecedentesFamiliares.objects.create(
                        paciente=paciente,
                        diabetes=random.choice([True, False]),
                        hipertension=random.choice([True, False]),
                        tuberculosis=random.choice([True, False]),
                        cardiopatia=random.choice([True, False]),
                    )

                    # ================= ANTECEDENTES OBSTÉTRICOS =================
                    gestas = random.randint(0, 5)
                    partos = random.randint(0, gestas)
                    abortos = random.randint(0, gestas - partos if gestas > partos else 0)

                    antecedentes_obstetricos = AntecedentesObstetricos(
                        paciente=paciente,
                        gestas=gestas,
                        partos=partos,
                        cesareas=random.randint(0, partos),
                        abortos=abortos,
                        nacidos_vivos=partos,
                        nacidos_muertos=0
                    )

                    antecedentes_obstetricos.full_clean()
                    antecedentes_obstetricos.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✔ {paciente.nombre_completo} | Usuario: {telefono} | Pass: {password}"
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error creando paciente {i}: {str(e)}")
                )

        self.stdout.write(
            self.style.SUCCESS("\n🔥 Pacientes de prueba creados correctamente.\n")
        )