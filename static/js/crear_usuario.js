/**
 * Script para el formulario de creación de usuarios
 * Maneja validaciones, interacciones y confirmaciones
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const form = document.getElementById('crearUsuarioForm');
    const usernameInput = document.getElementById('{{ form.username.id_for_label }}');
    const emailInput = document.getElementById('{{ form.email.id_for_label }}');
    const roleSelect = document.getElementById('{{ form.rol.id_for_label }}');
    const roleDescription = document.getElementById('role-description');
    const roleDescText = document.getElementById('role-desc-text');
    const btnLimpiar = document.getElementById('btn-limpiar');
    const btnSubmit = document.getElementById('btn-submit');
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    const confirmSubmitBtn = document.getElementById('confirm-submit');
    const modalUsername = document.getElementById('modal-username');
    const modalRole = document.getElementById('modal-role');
    
    // Feedback de username
    const usernameFeedback = document.getElementById('username-feedback');
    
    // Patrones de validación
    const patterns = {
        username: /^[a-zA-Z0-9._]{3,30}$/,
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        name: /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,50}$/
    };
    
    // Mensajes de error
    const errorMessages = {
        username: {
            required: 'El nombre de usuario es requerido',
            pattern: 'Solo letras, números y puntos. Mínimo 3 caracteres.',
            taken: 'Este nombre de usuario ya está en uso'
        },
        email: {
            required: 'El correo electrónico es requerido',
            pattern: 'Por favor ingrese un correo válido',
            taken: 'Este correo ya está registrado'
        },
        first_name: {
            required: 'El nombre es requerido',
            pattern: 'Solo letras y espacios. Mínimo 2 caracteres.'
        },
        last_name: {
            required: 'El apellido es requerido',
            pattern: 'Solo letras y espacios. Mínimo 2 caracteres.'
        },
        rol: {
            required: 'Debe seleccionar un rol'
        }
    };
    
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // ==================== VALIDACIONES ====================
    
    // Validación en tiempo real del username
    if (usernameInput) {
        let usernameTimeout;
        
        usernameInput.addEventListener('input', function() {
            clearTimeout(usernameTimeout);
            usernameTimeout = setTimeout(validateUsername, 500);
        });
        
        usernameInput.addEventListener('blur', validateUsername);
    }
    
    function validateUsername() {
        const value = usernameInput.value.trim();
        usernameFeedback.className = '';
        usernameFeedback.innerHTML = '';
        
        if (!value) {
            showFieldError(usernameInput, errorMessages.username.required);
            return false;
        }
        
        if (!patterns.username.test(value)) {
            showFieldError(usernameInput, errorMessages.username.pattern);
            return false;
        }
        
        // Verificar disponibilidad (simulada - en producción harías una petición AJAX)
        checkUsernameAvailability(value);
        
        return true;
    }
    
    function checkUsernameAvailability(username) {
        // Aquí iría una petición AJAX real al servidor
        // Por ahora simulamos una verificación
        setTimeout(() => {
            // Simulación: si el username contiene "admin", está ocupado
            if (username.toLowerCase().includes('admin')) {
                showFieldError(usernameInput, errorMessages.username.taken);
                usernameFeedback.className = 'invalid';
                usernameFeedback.innerHTML = '<i class="fas fa-times-circle me-1"></i> Este nombre de usuario no está disponible';
            } else {
                showFieldSuccess(usernameInput);
                usernameFeedback.className = 'valid';
                usernameFeedback.innerHTML = '<i class="fas fa-check-circle me-1"></i> Nombre de usuario disponible';
            }
        }, 300);
    }
    
    // Validación de email
    if (emailInput) {
        emailInput.addEventListener('blur', validateEmail);
    }
    
    function validateEmail() {
        const value = emailInput.value.trim();
        
        if (!value) {
            showFieldError(emailInput, errorMessages.email.required);
            return false;
        }
        
        if (!patterns.email.test(value)) {
            showFieldError(emailInput, errorMessages.email.pattern);
            return false;
        }
        
        showFieldSuccess(emailInput);
        return true;
    }
    
    // Validación de nombres
    function validateName(input, fieldName) {
        const value = input.value.trim();
        const messages = errorMessages[fieldName];
        
        if (!value) {
            showFieldError(input, messages.required);
            return false;
        }
        
        if (!patterns.name.test(value)) {
            showFieldError(input, messages.pattern);
            return false;
        }
        
        showFieldSuccess(input);
        return true;
    }
    
    // Validación de rol
    if (roleSelect) {
        roleSelect.addEventListener('change', function() {
            validateRole();
            updateRoleDescription();
        });
    }
    
    function validateRole() {
        if (!roleSelect.value) {
            showFieldError(roleSelect, errorMessages.rol.required);
            return false;
        }
        
        showFieldSuccess(roleSelect);
        return true;
    }
    
    function updateRoleDescription() {
        const selectedOption = roleSelect.options[roleSelect.selectedIndex];
        const description = selectedOption.getAttribute('data-description');
        
        if (description && description !== 'Sin descripción') {
            roleDescText.textContent = description;
            roleDescription.style.display = 'block';
        } else {
            roleDescription.style.display = 'none';
        }
    }
    
    // ==================== HELPERS DE VALIDACIÓN ====================
    
    function showFieldError(input, message) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        
        const feedback = input.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = message;
            feedback.style.display = 'block';
        }
    }
    
    function showFieldSuccess(input) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        
        const feedback = input.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.style.display = 'none';
        }
    }
    
    function resetFieldValidation(input) {
        input.classList.remove('is-invalid', 'is-valid');
        const feedback = input.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.style.display = 'none';
        }
    }
    
    // ==================== MANEJO DEL FORMULARIO ====================
    
    // Limpiar formulario
    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', function() {
            if (confirm('¿Está seguro de que desea limpiar todo el formulario? Se perderán todos los datos ingresados.')) {
                form.reset();
                
                // Resetear validaciones visuales
                document.querySelectorAll('.form-control, .form-select').forEach(input => {
                    resetFieldValidation(input);
                });
                
                // Ocultar descripción de rol
                if (roleDescription) {
                    roleDescription.style.display = 'none';
                }
                
                // Resetear feedback de username
                if (usernameFeedback) {
                    usernameFeedback.className = '';
                    usernameFeedback.innerHTML = '';
                }
                
                // Enfocar primer campo
                if (usernameInput) {
                    usernameInput.focus();
                }
            }
        });
    }
    
    // Validación antes de enviar
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Validar todos los campos
            const isUsernameValid = usernameInput ? validateUsername() : true;
            const isEmailValid = emailInput ? validateEmail() : true;
            const isRoleValid = roleSelect ? validateRole() : true;
            
            // Validar nombres
            const firstNameInput = document.getElementById('{{ form.first_name.id_for_label }}');
            const lastNameInput = document.getElementById('{{ form.last_name.id_for_label }}');
            const isFirstNameValid = firstNameInput ? validateName(firstNameInput, 'first_name') : true;
            const isLastNameValid = lastNameInput ? validateName(lastNameInput, 'last_name') : true;
            
            // Verificar si hay campos inválidos
            const invalidFields = form.querySelectorAll('.is-invalid');
            
            if (invalidFields.length > 0) {
                // Mostrar alerta general
                showAlert('Por favor corrija los errores en el formulario antes de continuar.', 'danger');
                
                // Desplazar al primer error
                invalidFields[0].scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
                
                return false;
            }
            
            // Mostrar modal de confirmación
            showConfirmationModal();
        });
    }
    
    // Mostrar modal de confirmación
    function showConfirmationModal() {
        // Llenar datos del modal
        if (modalUsername && usernameInput) {
            modalUsername.textContent = usernameInput.value;
        }
        
        if (modalRole && roleSelect) {
            const selectedOption = roleSelect.options[roleSelect.selectedIndex];
            modalRole.textContent = selectedOption.textContent;
        }
        
        // Mostrar modal
        confirmModal.show();
    }
    
    // Confirmar envío del formulario
    if (confirmSubmitBtn) {
        confirmSubmitBtn.addEventListener('click', function() {
            // Cambiar texto del botón a "Procesando..."
            const originalText = btnSubmit.innerHTML;
            btnSubmit.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';
            btnSubmit.disabled = true;
            
            // Cerrar modal
            confirmModal.hide();
            
            // Enviar formulario después de un breve delay
            setTimeout(() => {
                form.submit();
            }, 500);
        });
    }
    
    // ==================== FUNCIONES AUXILIARES ====================
    
    function showAlert(message, type = 'info') {
        // Crear alerta
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Insertar al principio del card-body
        const cardBody = document.querySelector('.card-body');
        if (cardBody) {
            const messagesDiv = cardBody.querySelector('.messages');
            if (messagesDiv) {
                messagesDiv.prepend(alertDiv);
            } else {
                cardBody.insertBefore(alertDiv, cardBody.firstChild);
            }
            
            // Auto-eliminar después de 5 segundos
            setTimeout(() => {
                if (alertDiv.parentElement) {
                    const bsAlert = new bootstrap.Alert(alertDiv);
                    bsAlert.close();
                }
            }, 5000);
        }
    }
    
    // ==================== INICIALIZACIÓN ====================
    
    // Inicializar validaciones
    if (usernameInput) validateUsername();
    if (emailInput) validateEmail();
    if (roleSelect) {
        validateRole();
        updateRoleDescription();
    }
    
    // Validar nombres al perder foco
    const firstNameInput = document.getElementById('{{ form.first_name.id_for_label }}');
    const lastNameInput = document.getElementById('{{ form.last_name.id_for_label }}');
    
    if (firstNameInput) {
        firstNameInput.addEventListener('blur', function() {
            validateName(this, 'first_name');
        });
    }
    
    if (lastNameInput) {
        lastNameInput.addEventListener('blur', function() {
            validateName(this, 'last_name');
        });
    }
    
    // Prevenir envío con Enter en campos individuales
    document.querySelectorAll('input:not([type="submit"])').forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                
                // Encontrar siguiente campo
                const formElements = Array.from(form.elements);
                const currentIndex = formElements.indexOf(this);
                const nextElement = formElements[currentIndex + 1];
                
                if (nextElement) {
                    nextElement.focus();
                    
                    // Si es un select, abrir el dropdown
                    if (nextElement.tagName === 'SELECT') {
                        nextElement.click();
                    }
                }
            }
        });
    });
    
    // Efecto de hover en secciones
    document.querySelectorAll('.form-section').forEach(section => {
        section.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        section.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    console.log('Script de creación de usuarios cargado correctamente');
});