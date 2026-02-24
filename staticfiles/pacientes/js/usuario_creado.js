/**
 * Script para la página de confirmación de usuario creado
 * Maneja interacciones, copiado de contraseña, etc.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const tempPassword = document.getElementById('temp-password');
    const copyPasswordBtn = document.getElementById('copy-password');
    const showPasswordBtn = document.getElementById('show-password');
    const copyFeedback = document.getElementById('copy-feedback');
    const generateQrBtn = document.getElementById('generate-qr');
    const qrPlaceholder = document.querySelector('.qr-code-placeholder');
    
    // Modal de Bootstrap
    const newPasswordModal = new bootstrap.Modal(document.getElementById('newPasswordModal'));
    
    // ==================== FUNCIONALIDAD DE CONTRASEÑA ====================
    
    // Copiar contraseña al portapapeles
    if (copyPasswordBtn && tempPassword) {
        copyPasswordBtn.addEventListener('click', function() {
            copyToClipboard(tempPassword.value);
            
            // Mostrar feedback
            copyFeedback.style.display = 'block';
            copyPasswordBtn.innerHTML = '<i class="fas fa-check"></i>';
            copyPasswordBtn.classList.remove('btn-outline-secondary');
            copyPasswordBtn.classList.add('btn-success');
            
            // Resetear después de 3 segundos
            setTimeout(() => {
                copyFeedback.style.display = 'none';
                copyPasswordBtn.innerHTML = '<i class="fas fa-copy"></i>';
                copyPasswordBtn.classList.remove('btn-success');
                copyPasswordBtn.classList.add('btn-outline-secondary');
            }, 3000);
        });
    }
    
    // Mostrar/ocultar contraseña
    if (showPasswordBtn && tempPassword) {
        let passwordVisible = false;
        
        showPasswordBtn.addEventListener('click', function() {
            passwordVisible = !passwordVisible;
            
            if (passwordVisible) {
                tempPassword.type = 'text';
                showPasswordBtn.innerHTML = '<i class="fas fa-eye-slash"></i>';
                showPasswordBtn.classList.remove('btn-outline-secondary');
                showPasswordBtn.classList.add('btn-warning');
            } else {
                tempPassword.type = 'text'; // Ya es text, pero por si acaso
                showPasswordBtn.innerHTML = '<i class="fas fa-eye"></i>';
                showPasswordBtn.classList.remove('btn-warning');
                showPasswordBtn.classList.add('btn-outline-secondary');
            }
        });
    }
    
    // Función para copiar al portapapeles
    function copyToClipboard(text) {
        // Crear elemento temporal
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            console.log('Contraseña copiada: ' + (successful ? 'éxito' : 'fallo'));
        } catch (err) {
            console.error('Error al copiar: ', err);
        }
        
        document.body.removeChild(textArea);
    }
    
    // ==================== GENERAR NUEVA CONTRASEÑA ====================
    
    window.generateNewPassword = function() {
        newPasswordModal.show();
    };
    
    window.confirmNewPassword = function() {
        // Aquí iría la petición AJAX al servidor para generar nueva contraseña
        // Por ahora simulamos la generación
        
        // Mostrar loading
        const generateBtn = document.querySelector('#newPasswordModal .btn-danger');
        const originalText = generateBtn.innerHTML;
        generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generando...';
        generateBtn.disabled = true;
        
        // Simular petición AJAX
        setTimeout(() => {
            // Generar nueva contraseña (simulada)
            const newPassword = generateRandomPassword(12);
            
            // Actualizar en la interfaz
            if (tempPassword) {
                tempPassword.value = newPassword;
            }
            
            // Actualizar en la tarjeta de credenciales
            const credencialPassword = document.querySelector('#credencial-card .text-danger');
            if (credencialPassword) {
                credencialPassword.textContent = newPassword;
            }
            
            // Cerrar modal
            newPasswordModal.hide();
            
            // Resetear botón
            generateBtn.innerHTML = originalText;
            generateBtn.disabled = false;
            
            // Mostrar notificación de éxito
            showNotification('¡Nueva contraseña generada!', 'success');
            
        }, 1500);
    };
    
    function generateRandomPassword(length) {
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*";
        let password = "";
        
        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * charset.length);
            password += charset[randomIndex];
        }
        
        return password;
    }
    
    // ==================== GENERAR QR ====================
    
    if (generateQrBtn && qrPlaceholder) {
        generateQrBtn.addEventListener('click', function() {
            // Aquí iría la generación real del QR
            // Por ahora simulamos con un cambio visual
            
            generateQrBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generando...';
            generateQrBtn.disabled = true;
            
            setTimeout(() => {
                qrPlaceholder.innerHTML = `
                    <div class="qr-code-generated">
                        <div class="qr-code" style="width: 150px; height: 150px; margin: 0 auto; background: #000; position: relative;">
                            <!-- Patrón simulado de QR -->
                            <div style="position: absolute; top: 10px; left: 10px; width: 30px; height: 30px; background: #fff;"></div>
                            <div style="position: absolute; top: 10px; right: 10px; width: 30px; height: 30px; background: #fff;"></div>
                            <div style="position: absolute; bottom: 10px; left: 10px; width: 30px; height: 30px; background: #fff;"></div>
                        </div>
                        <p class="mt-2 small">QR generado para acceso rápido</p>
                        <button class="btn btn-sm btn-outline-primary mt-2" onclick="downloadQR()">
                            <i class="fas fa-download me-1"></i>Descargar QR
                        </button>
                    </div>
                `;
                
                generateQrBtn.style.display = 'none';
                
            }, 1000);
        });
    }
    
    window.downloadQR = function() {
        // Aquí iría la lógica para descargar el QR
        showNotification('QR descargado exitosamente', 'info');
    };
    
    // ==================== ENVIAR CREDENCIALES POR EMAIL ====================
    
    window.sendCredentialsEmail = function() {
        // Mostrar confirmación
        if (confirm('¿Enviar las credenciales por correo electrónico al usuario?')) {
            // Aquí iría la petición AJAX al servidor
            // Por ahora simulamos el envío
            
            const sendBtn = document.querySelector('[onclick="sendCredentialsEmail()"]');
            const originalText = sendBtn.innerHTML;
            
            sendBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...';
            sendBtn.disabled = true;
            
            setTimeout(() => {
                sendBtn.innerHTML = originalText;
                sendBtn.disabled = false;
                
                showNotification('¡Credenciales enviadas por email exitosamente!', 'success');
                
            }, 2000);
        }
    };
    
    // ==================== FUNCIONES AUXILIARES ====================
    
    function showNotification(message, type = 'info') {
        // Crear notificación
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15);
        `;
        
        const icon = type === 'success' ? 'check-circle' : 
                    type === 'warning' ? 'exclamation-triangle' : 
                    type === 'danger' ? 'times-circle' : 'info-circle';
        
        notification.innerHTML = `
            <i class="fas fa-${icon} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-eliminar después de 5 segundos
        setTimeout(() => {
            if (notification.parentElement) {
                const bsAlert = new bootstrap.Alert(notification);
                bsAlert.close();
            }
        }, 5000);
    }
    
    // ==================== IMPRESIÓN MEJORADA ====================
    
    // Configurar evento de impresión
    window.addEventListener('beforeprint', function() {
        // Agregar información adicional para imprimir
        const printHeader = document.createElement('div');
        printHeader.className = 'print-header';
        printHeader.innerHTML = `
            <div style="text-align: center; margin-bottom: 20px; border-bottom: 2px solid #000; padding-bottom: 10px;">
                <h2>Credenciales de Usuario - Sistema Médico</h2>
                <p>Fecha de emisión: {% now "d/m/Y H:i" %}</p>
            </div>
        `;
        
        document.body.insertBefore(printHeader, document.body.firstChild);
    });
    
    window.addEventListener('afterprint', function() {
        // Limpiar elementos de impresión
        const printHeader = document.querySelector('.print-header');
        if (printHeader) {
            printHeader.remove();
        }
    });
    
    // ==================== INICIALIZACIÓN ====================
    
    console.log('Página de usuario creado cargada correctamente');
    
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});