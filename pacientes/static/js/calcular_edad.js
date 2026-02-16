// función para calcular edad a partir de fecha de nacimiento
function calcularEdad(fechaNacimiento) {
    if (!fechaNacimiento) return null;
    
    const hoy = new Date();
    const nacimiento = new Date(fechaNacimiento);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const mes = hoy.getMonth() - nacimiento.getMonth();
    
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--;
    }
    return edad;
}

// función principal que se ejecuta al cambiar la fecha
function manejarEdadPaciente() {
    const fechaInput = document.getElementById('fecha_nacimiento');
    const edadInput = document.getElementById('edad');
    const tutorTab = document.getElementById('tutor-tab');
    const tutorAlert = document.getElementById('tutorAlert');
    const minorAlert = document.getElementById('minorAlert');
    const minorWarning = document.getElementById('minorWarning');
    const ageStatus = document.getElementById('ageStatus');
    
    if (!fechaInput) return;
    
    fechaInput.addEventListener('change', function() {
        const fecha = this.value;
        const edad = calcularEdad(fecha);
        
        // Actualizar campo de edad
        if (edadInput) {
            edadInput.value = edad || '';
        }
        
        // Determinar si es menor de edad (18 años)
        const esMenor = edad < 18;
        
        // Actualizar estado visual
        if (ageStatus) {
            if (esMenor) {
                ageStatus.innerHTML = '<span class="badge bg-warning"><i class="fas fa-child me-1"></i>Menor de edad</span>';
            } else {
                ageStatus.innerHTML = '<span class="badge bg-success"><i class="fas fa-user-check me-1"></i>Mayor de edad</span>';
            }
        }
        
        // Mostrar/ocultar alertas para menores
        if (minorAlert) {
            if (esMenor) {
                minorAlert.classList.remove('d-none');
            } else {
                minorAlert.classList.add('d-none');
            }
        }
        
        if (minorWarning) {
            if (esMenor) {
                minorWarning.classList.remove('d-none');
            } else {
                minorWarning.classList.add('d-none');
            }
        }
        
        // Manejar la pestaña de Responsable Legal
        if (tutorTab) {
            const badge = tutorTab.querySelector('.badge');
            
            if (esMenor) {
                // Habilitar pestaña para menores
                tutorTab.classList.remove('disabled');
                tutorTab.style.pointerEvents = 'auto';
                tutorTab.style.opacity = '1';
                
                // Actualizar alerta
                if (tutorAlert) {
                    tutorAlert.classList.remove('d-none');
                    tutorAlert.innerHTML = '<i class="fas fa-exclamation-circle me-2"></i>Esta sección es obligatoria para pacientes menores de edad.';
                }
                
                // Actualizar badge
                if (badge) {
                    badge.classList.remove('bg-secondary');
                    badge.classList.add('bg-warning');
                    badge.textContent = '3';
                }
            } else {
                // Deshabilitar pestaña para mayores
                tutorTab.classList.add('disabled');
                tutorTab.style.pointerEvents = 'none';
                tutorTab.style.opacity = '0.6';
                
                // Actualizar alerta
                if (tutorAlert) {
                    tutorAlert.classList.remove('d-none');
                    tutorAlert.classList.remove('alert-warning');
                    tutorAlert.classList.add('alert-info');
                    tutorAlert.innerHTML = '<i class="fas fa-info-circle me-2"></i>Esta sección no es requerida para pacientes mayores de edad. Los campos son opcionales.';
                }
                
                // Actualizar badge
                if (badge) {
                    badge.classList.remove('bg-warning');
                    badge.classList.add('bg-secondary');
                    badge.textContent = '3';
                }
            }
        }
    });
    
    // Ejecutar al cargar si ya hay una fecha
    if (fechaInput.value) {
        fechaInput.dispatchEvent(new Event('change'));
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', manejarEdadPaciente);