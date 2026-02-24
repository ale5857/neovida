from django.db import models
from expedientes.models import Embarazo
from usuarios.models import Usuario


class ConsultaPrenatal(models.Model):
    """
    Control prenatal completo basado en evaluación obstétrica real
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
    # NUMERO AUTOMATICO DE CONTROL
    # ======================
    numero_control = models.PositiveIntegerField(editable=False)

    # ======================
    # DATOS GENERALES
    # ======================
    fecha_consulta = models.DateField(auto_now_add=True)
    semana_gestacion = models.PositiveIntegerField()

    motivo_consulta = models.CharField(max_length=255)
    atendida = models.BooleanField(default=False)

    # ======================
    # SIGNOS VITALES MATERNOS
    # ======================
    peso_madre = models.DecimalField(max_digits=5, decimal_places=2)

    presion_sistolica = models.PositiveIntegerField()
    presion_diastolica = models.PositiveIntegerField()

    frecuencia_cardiaca_materna = models.PositiveIntegerField()
    frecuencia_respiratoria = models.PositiveIntegerField()
    temperatura = models.DecimalField(max_digits=4, decimal_places=1)

    edema = models.BooleanField(default=False)
    proteinuria = models.BooleanField(default=False)

    # ======================
    # EVALUACIÓN FETAL
    # ======================
    altura_uterina = models.DecimalField(max_digits=5, decimal_places=2)
    frecuencia_cardiaca_fetal = models.PositiveIntegerField()

    movimientos_fetales = models.BooleanField()
    movimientos_disminuidos = models.BooleanField(default=False)
    ausencia_movimientos = models.BooleanField(default=False)

    presentacion_fetal = models.CharField(
        max_length=50,
        choices=[
            ('cefálica', 'Cefálica'),
            ('podálica', 'Podálica'),
            ('transversa', 'Transversa'),
            ('no_determinada', 'No determinada'),
        ],
        default='no_determinada'
    )

    # ======================
    # SIGNOS Y SÍNTOMAS
    # ======================
    sintomas = models.TextField()
    signos_clinicos = models.TextField()
    signos_alarma = models.TextField()

    # ======================
    # FACTORES DE RIESGO
    # ======================
    diabetes_gestacional = models.BooleanField(default=False)
    hipertension_gestacional = models.BooleanField(default=False)

    antecedentes_patologicos = models.TextField(blank=True)
    consumo_medicamentos = models.TextField(blank=True)
    consumo_drogas = models.BooleanField(default=False)

    # ======================
    # EDAD GESTACIONAL
    # ======================
    calculado_por = models.CharField(
        max_length=10,
        choices=[
            ('fur', 'Fecha última regla'),
            ('usg', 'Ultrasonido')
        ],
        default='fur'
    )

    semanas_por_ultrasonido = models.PositiveIntegerField(null=True, blank=True)

    # ======================
    # DIAGNÓSTICO Y CONDUCTA
    # ======================
    impresion_clinica = models.TextField()
    recomendaciones = models.TextField()
    tratamiento = models.TextField()

    proxima_cita = models.DateTimeField()

    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_consulta']

    # ======================
    # SAVE AUTOMATICO
    # ======================
    def save(self, *args, **kwargs):
        if not self.pk:
            ultimo = ConsultaPrenatal.objects.filter(
                embarazo=self.embarazo
            ).count()

            self.numero_control = ultimo + 1

        super().save(*args, **kwargs)


        

    # ======================
    # LOGICA CLINICA
    # ======================

    def tipo_parto_probable(self):
        if self.semana_gestacion < 37:
            return "Pretérmino"
        elif 37 <= self.semana_gestacion <= 41:
            return "A término"
        else:
            return "Postérmino"

    def es_hipertension(self):
        return self.presion_sistolica >= 140 or self.presion_diastolica >= 90

    def es_fiebre(self):
        return self.temperatura >= 38

    def riesgo_obstetrico(self):
        """
        Clasificación tipo sistema Galeno:
        Verde = Bajo riesgo
        Amarillo = Moderado
        Rojo = Alto riesgo
        """

        if (
            self.ausencia_movimientos
            or self.es_hipertension()
            or self.diabetes_gestacional
            or self.hipertension_gestacional
            or self.es_fiebre()
        ):
            return "ALTO"

        if self.movimientos_disminuidos:
            return "MODERADO"

        return "BAJO"

    def __str__(self):
        return f"Control #{self.numero_control} - {self.embarazo.expediente.paciente}"
    
    @property
    def alerta_critica(self):
           fcf = self.frecuencia_cardiaca_fetal or 0
           sist = self.presion_sistolica or 0
           diast = self.presion_diastolica or 0
           temp = self.temperatura or 0

           return (
           fcf < 120
           or fcf > 160
           or sist >= 140
           or diast >= 90
           or temp >= 38
           or self.ausencia_movimientos
             )