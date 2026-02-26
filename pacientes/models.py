from datetime import date

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from usuarios.models import Usuario


class Paciente(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='paciente',
        null=True,
        blank=True
    )

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    domicilio = models.CharField(max_length=255)
    localidad = models.CharField(max_length=100)

    telefono = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{8}$',
                message="El teléfono debe tener exactamente 8 dígitos numéricos."
            )
        ]
    )

    raza = models.CharField(max_length=20, blank=True, null=True)
    estado_civil = models.CharField(max_length=20)
    escolaridad = models.CharField(max_length=50)

    creado_en = models.DateTimeField(auto_now_add=True)

    # ================= PROPIEDADES =================

    @property
    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) <
            (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    # ================= VALIDACIONES =================

    def clean(self):
        if self.edad < 12:
            raise ValidationError(
                "La paciente debe tener al menos 12 años."
            )

    def __str__(self):
        return self.nombre_completo


# =======================================================
# ANTECEDENTES PERSONALES
# =======================================================

class AntecedentesPersonales(models.Model):

    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='antecedentes_personales'
    )

    tuberculosis = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    hipertension = models.BooleanField(default=False)
    cardiopatia = models.BooleanField(default=False)
    nefropatia = models.BooleanField(default=False)
    asma = models.BooleanField(default=False)

    vih = models.BooleanField(default=False)
    sifilis = models.BooleanField(default=False)

    preeclampsia = models.BooleanField(default=False)
    eclampsia = models.BooleanField(default=False)

    cirugias_previas = models.TextField(blank=True, null=True)
    otras_enfermedades = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Antecedentes personales - {self.paciente.nombre_completo}"


# =======================================================
# ANTECEDENTES FAMILIARES
# =======================================================

class AntecedentesFamiliares(models.Model):

    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='antecedentes_familiares'
    )

    diabetes = models.BooleanField(default=False)
    hipertension = models.BooleanField(default=False)
    tuberculosis = models.BooleanField(default=False)
    cardiopatia = models.BooleanField(default=False)

    otras_enfermedades = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Antecedentes familiares - {self.paciente.nombre_completo}"


# =======================================================
# ANTECEDENTES OBSTÉTRICOS
# =======================================================

class AntecedentesObstetricos(models.Model):

    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='antecedentes_obstetricos'
    )

    gestas = models.PositiveIntegerField(default=0)
    partos = models.PositiveIntegerField(default=0)
    cesareas = models.PositiveIntegerField(default=0)
    abortos = models.PositiveIntegerField(default=0)

    nacidos_vivos = models.PositiveIntegerField(default=0)
    nacidos_muertos = models.PositiveIntegerField(default=0)

    peso_ultimo_rn = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    complicaciones_previas = models.TextField(blank=True, null=True)

    # ================= VALIDACIONES MÉDICAS =================

    def clean(self):

        if self.partos > self.gestas:
            raise ValidationError(
                "Los partos no pueden ser mayores que las gestas."
            )

        if self.abortos > self.gestas:
            raise ValidationError(
                "Los abortos no pueden ser mayores que las gestas."
            )

        if self.nacidos_vivos + self.nacidos_muertos > self.partos:
            raise ValidationError(
                "Los nacidos vivos y muertos no pueden superar el número de partos."
            )

    def __str__(self):
        return f"Antecedentes obstétricos - {self.paciente.nombre_completo}"