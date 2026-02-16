from django.db import models
from pacientes.models import Paciente


class Expediente(models.Model):
    """
    Expediente clínico de la paciente.
    Es único por paciente.
    """

    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='expediente'
    )

    fecha_apertura = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=30,
        default='Activo'
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Expediente #{self.id} - {self.paciente}"

class Embarazo(models.Model):
    """
    Embarazo asociado a un expediente clínico.
    Una paciente puede tener varios embarazos,
    pero solo uno activo a la vez.
    """

    expediente = models.ForeignKey(
        Expediente,
        on_delete=models.CASCADE,
        related_name='embarazos'
    )

    fecha_ultima_regla = models.DateField()
    semanas_gestacion = models.PositiveIntegerField()

    peso_anterior = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    talla = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    embarazo_planeado = models.BooleanField(default=True)
    falla_metodo_anticonceptivo = models.BooleanField(default=False)

    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Garantiza que solo exista un embarazo activo
        por expediente.
        """
        if self.activo:
            Embarazo.objects.filter(
                expediente=self.expediente,
                activo=True
            ).exclude(id=self.id).update(activo=False)
        super().save(*args, **kwargs)

    def __str__(self):
        estado = "Activo" if self.activo else "Finalizado"
        return f"Embarazo #{self.id} ({estado}) - {self.expediente.paciente}"

class Vacuna(models.Model):
    """
    Vacunas aplicadas durante el embarazo (MINSA).
    """

    embarazo = models.ForeignKey(
        Embarazo,
        on_delete=models.CASCADE,
        related_name='vacunas'
    )

    nombre = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    dosis = models.CharField(max_length=50, blank=True, null=True)
    lote = models.CharField(max_length=50, blank=True, null=True)

    observaciones = models.TextField(blank=True, null=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.embarazo.expediente.paciente}"


class Laboratorio(models.Model):
    """
    Exámenes de laboratorio del control prenatal (MINSA).
    """

    embarazo = models.ForeignKey(
        Embarazo,
        on_delete=models.CASCADE,
        related_name='laboratorios'
    )

    fecha = models.DateField()

    # Hemoglobina
    hb_menor_20_sem = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True
    )

    hb_mayor_20_sem = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True
    )

    # Exámenes generales
    ego = models.BooleanField(default=False)  # Examen general de orina
    vih = models.BooleanField(default=False)
    sifilis = models.BooleanField(default=False)

    # Suplementación
    hierro = models.BooleanField(default=False)
    acido_folico = models.BooleanField(default=False)

    estreptococo_b = models.BooleanField(default=False)

    observaciones = models.TextField(blank=True, null=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Laboratorio {self.fecha} - {self.embarazo.expediente.paciente}"


class Ultrasonido(models.Model):
    """
    Ultrasonidos realizados durante el embarazo (MINSA).
    """

    embarazo = models.ForeignKey(
        Embarazo,
        on_delete=models.CASCADE,
        related_name='ultrasonidos'
    )

    fecha = models.DateField()
    semanas_gestacion = models.PositiveIntegerField()

    # Medidas fetales
    lcn = models.DecimalField(  # Longitud cráneo-nalga
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    diametro_biparietal = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    femur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    circunferencia_abdominal = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    peso_estimado = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
    )

    placenta = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    liquido_amniotico = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    hallazgos = models.TextField(blank=True, null=True)

    imagen = models.ImageField(
        upload_to='ultrasonidos/',
        blank=True,
        null=True
    )

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ultrasonido {self.fecha} - {self.embarazo.expediente.paciente}"