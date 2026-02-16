from django.db import models
from expedientes.models import Embarazo
from usuarios.models import Usuario


class ConsultaPrenatal(models.Model):
    """
    Consulta / control prenatal según normativa MINSA
    """

    # ======================
    # RELACIONES
    # ======================
    embarazo = models.ForeignKey(
        Embarazo,
        on_delete=models.CASCADE,
        related_name='consultas_prenatales'
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        help_text="Profesional de salud que realiza la consulta"
    )

    # ======================
    # DATOS GENERALES
    # ======================
    fecha_consulta = models.DateField(auto_now_add=True)
    semana_gestacion = models.PositiveIntegerField()

    atendida = models.BooleanField(
        default=False,
        help_text="Indica si la consulta fue atendida"
    )

    # ======================
    # SIGNOS VITALES MATERNOS
    # ======================
    peso_madre = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    presion_sistolica = models.PositiveIntegerField()
    presion_diastolica = models.PositiveIntegerField()

    edema = models.BooleanField(default=False)
    proteinuria = models.BooleanField(default=False)

    # ======================
    # EVALUACIÓN OBSTÉTRICA
    # ======================
    altura_uterina = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    frecuencia_cardiaca_fetal = models.PositiveIntegerField()
    movimientos_fetales = models.BooleanField()

    # ======================
    # EVALUACIÓN CLÍNICA
    # ======================
    sintomas = models.TextField()
    signos_alarma = models.TextField()
    impresion_clinica = models.TextField()

    # ======================
    # CONDUCTA
    # ======================
    recomendaciones = models.TextField()
    tratamiento = models.TextField()
    
    proxima_cita = models.DateTimeField(
    help_text="Fecha y hora de la próxima cita"
)


    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_consulta']

    def __str__(self):
        return f"Consulta {self.fecha_consulta} - {self.embarazo.expediente.paciente}"
