from django.db import models
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
    edad = models.PositiveIntegerField()

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    domicilio = models.CharField(max_length=255)
    localidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    raza = models.CharField(max_length=20, blank=True, null=True)
    estado_civil = models.CharField(max_length=20)
    escolaridad = models.CharField(max_length=50)


    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
 

class AntecedentesPersonales(models.Model):
    """
    Antecedentes personales patológicos según MINSA.
    """

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
        return f"Antecedentes personales - {self.paciente}"


class AntecedentesFamiliares(models.Model):
    """
    Antecedentes familiares según MINSA.
    """

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
        return f"Antecedentes familiares - {self.paciente}"


class AntecedentesObstetricos(models.Model):
    """
    Antecedentes obstétricos según MINSA.
    """

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

    def __str__(self):
        return f"Antecedentes obstétricos - {self.paciente}"
