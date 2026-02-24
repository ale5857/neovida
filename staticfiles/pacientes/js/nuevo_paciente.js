// nuevo_paciente.js - VERSIÓN QUE NUNCA FALLA
console.log('🔧 nuevo_paciente.js cargado');

// Función principal
function inicializarValidacion() {
    console.log('🔄 Inicializando validación...');
    
    // Buscar el formulario CORRECTO
    const form = document.getElementById('pacienteForm'); // pacienteForm NO patientForm
    
    if (!form) {
        console.warn('⚠️ No se encontró #pacienteForm en esta página.');
        console.log('ℹ️ Este script solo funciona en la página de nuevo paciente.');
        return;
    }
    
    console.log('✅ Formulario encontrado, configurando eventos...');
    
    // VALIDACIÓN AL GUARDAR
    form.addEventListener('submit', function(event) {
        console.log('📝 Validando formulario...');
        
        // Obtener campos obligatorios
        const requiredFields = form.querySelectorAll('[required]');
        let errores = [];
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                
                // Obtener nombre legible del campo
                let nombreCampo = field.name || 
                                 field.placeholder || 
                                 field.previousElementSibling?.textContent ||
                                 'Campo requerido';
                
                // Limpiar etiquetas HTML si las hay
                nombreCampo = nombreCampo.replace(/<[^>]*>/g, '').trim();
                errores.push(nombreCampo);
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        if (errores.length > 0) {
            event.preventDefault();
            console.warn('❌ Campos inválidos:', errores);
            
            let mensaje = 'Complete los siguientes campos obligatorios:\n\n';
            errores.forEach(error => {
                mensaje += `• ${error}\n`;
            });
            
            alert(mensaje);
            return false;
        }
        
        console.log('✅ Formulario válido, enviando...');
        
        // Confirmación opcional
        if (confirm('¿Está seguro de guardar la ficha prenatal?')) {
            return true;
        } else {
            event.preventDefault();
            return false;
        }
    });
    
    // SOLO NÚMEROS
    document.querySelectorAll('.solo-numeros').forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    });
    
    console.log('✅ Validación configurada correctamente');
}

// Múltiples formas de iniciar para asegurar
document.addEventListener('DOMContentLoaded', inicializarValidacion);

// Por si el DOM ya está cargado
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(inicializarValidacion, 100);
}

// Función global para números
function soloNumeros(e) {
    const teclasPermitidas = ['Backspace', 'Delete', 'Tab', 'ArrowLeft', 'ArrowRight'];
    
    if (!/^\d$/.test(e.key) && !teclasPermitidas.includes(e.key)) {
        e.preventDefault();
    }
}

// Bloqueo de pegado
document.addEventListener('paste', function(e) {
    if (e.target.classList.contains('solo-numeros')) {
        const texto = (e.clipboardData || window.clipboardData).getData('text');
        if (!/^\d+$/.test(texto)) {
            e.preventDefault();
            alert('⚠️ Solo puede pegar números en este campo');
        }
    }
});