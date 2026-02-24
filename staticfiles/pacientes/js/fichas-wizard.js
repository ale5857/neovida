// Archivo: static/pacientes/js/fichas-wizard.js
// Función para navegar entre fichas considerando la edad

document.addEventListener('DOMContentLoaded', function() {
    const navTabs = document.querySelectorAll('#patientTab .nav-link');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const nextButtons = document.querySelectorAll('.btn-siguiente');
    const prevButtons = document.querySelectorAll('.btn-anterior');
    const progressBar = document.getElementById('progress-bar');
    const pasoNumero = document.getElementById('paso-numero');
    const progresoTexto = document.getElementById('progreso-texto');
    const fichaActualNumero = document.getElementById('ficha-actual-numero');
    const botonGuardarFinal = document.getElementById('boton-guardar-final');
    const btnGuardarWizard = document.querySelector('.btn-guardar');
    const btnGuardarCompleto = document.querySelector('button[type="submit"].btn-custom-primary');

    // Función para obtener ficha actual
    function getCurrentFicha() {
        const activeTab = document.querySelector('#patientTab .nav-link.active');
        return activeTab ? parseInt(activeTab.getAttribute('data-ficha')) : 1;
    }

    // Función para verificar si es menor de edad
    function esPacienteMenor() {
        const edadInput = document.getElementById('edad');
        const edad = parseInt(edadInput.value) || 0;
        return edad < 18;
    }

    // Función para obtener siguiente ficha válida
    function getSiguienteFichaValida(currentFicha) {
        let siguiente = currentFicha + 1;
        
        // Si vamos a la ficha 3 (tutor) pero el paciente NO es menor, saltar a la 4
        if (siguiente === 3 && !esPacienteMenor()) {
            siguiente = 4;
        }
        
        // Asegurarse que no exceda el máximo
        const totalFichas = 5;
        return Math.min(siguiente, totalFichas);
    }

    // Función para obtener ficha anterior válida
    function getAnteriorFichaValida(currentFicha) {
        let anterior = currentFicha - 1;
        
        // Si vamos a la ficha 3 (tutor) pero el paciente NO es menor, regresar a la 2
        if (anterior === 3 && !esPacienteMenor()) {
            anterior = 2;
        }
        
        // Asegurarse que no sea menor a 1
        return Math.max(anterior, 1);
    }

    // Función para activar una ficha específica
    function activarFicha(numeroFicha) {
        // Desactivar todas
        navTabs.forEach(tab => {
            tab.classList.remove('active');
            tab.setAttribute('aria-selected', 'false');
        });
        
        tabPanes.forEach(pane => {
            pane.classList.remove('show', 'active');
        });
        
        // Activar la ficha específica
        const targetTab = document.querySelector(`#patientTab .nav-link[data-ficha="${numeroFicha}"]`);
        const targetPane = document.querySelector(`.tab-pane[role="tabpanel"]:nth-child(${numeroFicha})`);
        
        if (targetTab && targetPane) {
            targetTab.classList.add('active');
            targetTab.setAttribute('aria-selected', 'true');
            targetPane.classList.add('show', 'active');
            
            // Actualizar progreso
            const porcentaje = (numeroFicha / 5) * 100;
            if (progressBar) {
                progressBar.style.width = `${porcentaje}%`;
                progressBar.setAttribute('aria-valuenow', porcentaje);
            }
            
            if (pasoNumero) pasoNumero.textContent = numeroFicha;
            if (progresoTexto) progresoTexto.textContent = `${Math.round(porcentaje)}%`;
            if (fichaActualNumero) fichaActualNumero.textContent = numeroFicha;
            
            // Manejar visibilidad de botones
            const btnAnterior = targetPane.querySelector('.btn-anterior');
            const btnSiguiente = targetPane.querySelector('.btn-siguiente');
            
            if (btnAnterior) {
                btnAnterior.style.display = numeroFicha === 1 ? 'none' : 'block';
            }
            
            if (btnSiguiente) {
                btnSiguiente.style.display = numeroFicha === 5 ? 'none' : 'block';
            }
            
            // Mostrar botón de guardar final en la última ficha
            if (botonGuardarFinal) {
                botonGuardarFinal.style.display = numeroFicha === 5 ? 'block' : 'none';
            }
        }
    }

    // Event listeners para botones siguiente
    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentFicha = getCurrentFicha();
            
            // Validar campos requeridos antes de avanzar
            if (!validarFichaActual(currentFicha)) {
                return;
            }
            
            const siguienteFicha = getSiguienteFichaValida(currentFicha);
            activarFicha(siguienteFicha);
        });
    });

    // Event listeners para botones anterior
    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentFicha = getCurrentFicha();
            const anteriorFicha = getAnteriorFichaValida(currentFicha);
            activarFicha(anteriorFicha);
        });
    });

    // Event listener para tabs de navegación
    navTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            if (this.classList.contains('disabled')) {
                e.preventDefault();
                return;
            }
            
            const fichaNumero = parseInt(this.getAttribute('data-ficha'));
            
            // Si intentan ir a la ficha 3 (tutor) y NO es menor, saltar a la 4
            if (fichaNumero === 3 && !esPacienteMenor()) {
                activarFicha(4);
                return;
            }
            
            // Validar que se puedan saltar fichas en orden
            const currentFicha = getCurrentFicha();
            if (Math.abs(fichaNumero - currentFicha) > 1) {
                // Solo permitir saltos si la ficha intermedia está deshabilitada
                if (fichaNumero === 4 && currentFicha === 2 && !esPacienteMenor()) {
                    // Permitir salto de 2 a 4 cuando tutor no es requerido
                    activarFicha(4);
                    return;
                }
                
                // Para otros casos, mostrar mensaje
                alert('Por favor complete las fichas en orden.');
                return;
            }
            
            activarFicha(fichaNumero);
        });
    });

    // Event listener para botón guardar del wizard
    if (btnGuardarWizard) {
        btnGuardarWizard.addEventListener('click', function() {
            // Validar todas las fichas antes de enviar
            if (validarTodasLasFichas()) {
                // Mostrar confirmación
                if (confirm('¿Está seguro que desea guardar la ficha del paciente?')) {
                    document.getElementById('pacienteForm').submit();
                }
            }
        });
    }

    // Función para validar ficha actual
    function validarFichaActual(fichaNumero) {
        const pane = document.querySelector(`.tab-pane[role="tabpanel"]:nth-child(${fichaNumero})`);
        const requiredFields = pane.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('is-invalid');
                
                // Mostrar mensaje de error
                const feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                feedback.textContent = 'Este campo es requerido';
                
                const parent = field.parentElement;
                if (!parent.querySelector('.invalid-feedback')) {
                    parent.appendChild(feedback);
                }
            } else {
                field.classList.remove('is-invalid');
                const feedback = field.parentElement.querySelector('.invalid-feedback');
                if (feedback) {
                    feedback.remove();
                }
            }
        });
        
        // Validaciones específicas para ficha 3 (tutor) si es menor
        if (fichaNumero === 3 && esPacienteMenor()) {
            const tutorNombre = document.getElementById('tutor_nombre');
            const tutorParentesco = document.getElementById('tutor_parentesco');
            const consentimiento = document.getElementById('consentimiento');
            
            if (!tutorNombre.value.trim()) {
                isValid = false;
                tutorNombre.classList.add('is-invalid');
            }
            
            if (!tutorParentesco.value) {
                isValid = false;
                tutorParentesco.classList.add('is-invalid');
            }
            
            if (!consentimiento.checked) {
                isValid = false;
                consentimiento.classList.add('is-invalid');
                alert('Para pacientes menores de edad es necesario el consentimiento informado del responsable legal.');
            }
        }
        
        if (!isValid) {
            alert('Por favor complete todos los campos requeridos antes de continuar.');
        }
        
        return isValid;
    }

    // Función para validar todas las fichas
    function validarTodasLasFichas() {
        for (let i = 1; i <= 5; i++) {
            // Saltar validación de ficha 3 si no es menor
            if (i === 3 && !esPacienteMenor()) {
                continue;
            }
            
            if (!validarFichaActual(i)) {
                // Ir a la ficha con error
                activarFicha(i);
                return false;
            }
        }
        return true;
    }

    // Inicializar primera ficha
    activarFicha(1);
});
// fichas-wizard.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ fichas-wizard.js cargado');
    
    // Manejo del wizard
    const tabs = document.querySelectorAll('[data-ficha]');
    const progressBar = document.getElementById('progress-bar');
    const pasoNumero = document.getElementById('paso-numero');
    const progresoTexto = document.getElementById('progreso-texto');
    const fichaActualNumero = document.getElementById('ficha-actual-numero');
    
    if (!tabs.length) {
        console.warn('⚠️ No se encontraron tabs');
        return;
    }
    
    // Botones de navegación
    document.querySelectorAll('.btn-siguiente').forEach(btn => {
        btn.addEventListener('click', function() {
            const currentTab = document.querySelector('.tab-pane.active');
            if (!currentTab) return;
            
            // Validar campos obligatorios
            let valid = true;
            const requiredFields = currentTab.querySelectorAll(
                'input[required], select[required], textarea[required]'
            );
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    valid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!valid) {
                alert('⚠️ Complete los campos obligatorios antes de continuar.');
                return;
            }
            
            const currentTabId = currentTab.id;
            const nextTab = document.getElementById(getNextTab(currentTabId));
            
            if (nextTab) {
                const nextTabButton = document.querySelector(`[data-ficha="${nextTab.id}"]`);
                if (nextTabButton) {
                    nextTabButton.click();
                    updateProgress(nextTab.id);
                }
            }
        });
    });
    
    document.querySelectorAll('.btn-anterior').forEach(btn => {
        btn.addEventListener('click', function() {
            const currentTab = document.querySelector('.tab-pane.active');
            if (!currentTab) return;
            
            const currentTabId = currentTab.id;
            const prevTab = document.getElementById(getPrevTab(currentTabId));
            
            if (prevTab) {
                const prevTabButton = document.querySelector(`[data-ficha="${prevTab.id}"]`);
                if (prevTabButton) {
                    prevTabButton.click();
                    updateProgress(prevTab.id);
                }
            }
        });
    });
    
    // Botón Guardar del wizard (pestaña 5)
    document.querySelector('.btn-guardar')?.addEventListener('click', function() {
        // Validar todos los campos antes de enviar
        const form = document.getElementById('pacienteForm');
        if (!form) return;
        
        const allRequiredFields = form.querySelectorAll(
            'input[required], select[required], textarea[required]'
        );
        
        let allValid = true;
        
        allRequiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                allValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        if (!allValid) {
            alert('⚠️ Complete todos los campos obligatorios antes de guardar.');
            return;
        }
        
        form.submit();
    });
    
    // Función para obtener siguiente tab
    function getNextTab(currentId) {
        const tabOrder = ['personal', 'contact', 'tutor', 'medical', 'obstetric'];
        const currentIndex = tabOrder.indexOf(currentId);
        return tabOrder[currentIndex + 1] || currentId;
    }
    
    // Función para obtener tab anterior
    function getPrevTab(currentId) {
        const tabOrder = ['personal', 'contact', 'tutor', 'medical', 'obstetric'];
        const currentIndex = tabOrder.indexOf(currentId);
        return tabOrder[currentIndex - 1] || currentId;
    }
    
    // Actualizar progreso
    function updateProgress(tabId) {
        const tabOrder = ['personal', 'contact', 'tutor', 'medical', 'obstetric'];
        const currentIndex = tabOrder.indexOf(tabId);
        const progress = ((currentIndex + 1) / tabOrder.length) * 100;
        
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);
        }
        
        if (pasoNumero) {
            pasoNumero.textContent = currentIndex + 1;
        }
        
        if (progresoTexto) {
            progresoTexto.textContent = `${Math.round(progress)}%`;
        }
        
        if (fichaActualNumero) {
            fichaActualNumero.textContent = currentIndex + 1;
        }
        
        // Mostrar/ocultar botones según la ficha
        const isFirstTab = currentIndex === 0;
        const isLastTab = currentIndex === tabOrder.length - 1;
        
        // Mostrar botón anterior excepto en primera ficha
        document.querySelectorAll('.btn-anterior').forEach(btn => {
            btn.style.display = isFirstTab ? 'none' : 'inline-block';
        });
        
        // Mostrar botón siguiente excepto en última ficha
        document.querySelectorAll('.btn-siguiente').forEach(btn => {
            btn.style.display = isLastTab ? 'none' : 'inline-block';
        });
    }
    
    // Limpiar formulario
    document.getElementById('limpiar-todo')?.addEventListener('click', function() {
        if (confirm('¿Está seguro de que desea limpiar todo el formulario? Se perderán todos los datos ingresados.')) {
            document.getElementById('pacienteForm')?.reset();
            // Volver a la primera pestaña
            const firstTab = document.querySelector('[data-ficha="1"]');
            if (firstTab) firstTab.click();
            updateProgress('personal');
        }
    });
    
    // Bootstrap tab switching
    tabs.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-ficha');
            const tabOrder = ['personal', 'contact', 'tutor', 'medical', 'obstetric'];
            const tabIndex = parseInt(tabId) - 1;
            const tabPaneId = tabOrder[tabIndex];
            
            if (tabPaneId) {
                updateProgress(tabPaneId);
            }
        });
    });
    
    // Inicializar
    updateProgress('personal');
    console.log('✅ Wizard inicializado correctamente');
});