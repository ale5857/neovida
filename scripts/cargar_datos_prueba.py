from django.utils import timezone
from datetime import timedelta

from usuarios.models import Usuario
from pacientes.models import Paciente
from expedientes.models import Expediente, Embarazo
from citas.models import Cita

print("Iniciando carga de datos de prueba...")

# =========================
# OBTENER DOCTOR
# =========================
doctor = Usuario.objects.filter(rol='DOCTOR').first()
if not doctor:
    print("No existe un usuario con rol DOCTOR")
    exit()

# =========================
# OBTENER PACIENTE
# =========================
paciente = Paciente.objects.first()
if not paciente:
    print("No existe ningún paciente")
    exit()

# =========================
# EXPEDIENTE
# =========================
expediente, _ = Expediente.objects.get_or_create(
    paciente=paciente
)

# =========================
# EMBARAZO (SIN 'riesgo')
# =========================
embarazo, _ = Embarazo.objects.get_or_create(
    expediente=expediente,
    activo=True,
    defaults={
        'fecha_ultima_regla': timezone.now().date() - timedelta(days=70),
        'semanas_gestacion': 10
    }
)

# =========================
# CITAS (SEMANA COMPLETA)
# =========================
for i in range(5):
    fecha = timezone.now().date() + timedelta(days=i)

    Cita.objects.get_or_create(
        usuario=doctor,
        embarazo=embarazo,
        fecha=fecha
    )

print("Datos de prueba creados correctamente")
