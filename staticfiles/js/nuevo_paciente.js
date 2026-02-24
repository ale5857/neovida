document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('#patientTab button[data-bs-toggle="tab"]');
    const form = document.getElementById('patientForm');

    tabs.forEach(tab => {
        tab.addEventListener('click', function(event) {
            const currentTab = document.querySelector('.tab-pane.active');
            let valid = true;

            // Validar inputs requeridos en la pestaña actual
            const requiredFields = currentTab.querySelectorAll('input[required], select[required], textarea[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    valid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                event.preventDefault();
                alert('Complete los campos obligatorios antes de continuar.');
            }
        });
    });

    // Validación al guardar
    form.addEventListener('submit', function(event) {
        const allRequiredFields = form.querySelectorAll('input[required], select[required], textarea[required]');
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
            event.preventDefault();
            alert('Por favor, complete todos los campos obligatorios antes de guardar.');
        }
    });

    /* =====================================================
       🔒 BLOQUEO REAL DE LETRAS – SOLO NÚMEROS (SOLUCIÓN)
       ===================================================== */
    document.querySelectorAll(".solo-numeros").forEach(input => {

        input.addEventListener("input", function () {
            // Elimina cualquier letra o símbolo
            this.value = this.value.replace(/[^0-9]/g, "");
        });

    });
});

/* =====================================================
   🔒 FUNCIÓN (SE DEJA POR COMPATIBILIDAD, NO ES CLAVE)
   ===================================================== */
function soloNumeros(e) {
    const key = e.key;

    if (
        key === "Backspace" ||
        key === "Delete" ||
        key === "Tab" ||
        key === "ArrowLeft" ||
        key === "ArrowRight"
    ) {
        return;
    }

    if (!/^[0-9]$/.test(key)) {
        e.preventDefault();
    }
}

/* =====================================================
   🚫 BLOQUEO DE PEGADO CON LETRAS
   ===================================================== */
document.addEventListener("paste", function (e) {
    if (e.target.classList.contains("solo-numeros")) {
        let texto = (e.clipboardData || window.clipboardData).getData("text");
        if (!/^\d+$/.test(texto)) {
            e.preventDefault();
        }
    }
});
