// ===============================
// DATOS DESDE DJANGO
// ===============================
const data = JSON.parse(document.getElementById('expediente-data').textContent);

const expedienteId = data.expedienteId;
const pacienteNombre = data.pacienteNombre;
const totalConsultas = data.totalConsultas;
const embarazoId = data.embarazoId;


// ===============================
// FUNCIONES PRINCIPALES
// ===============================

function nuevaConsulta() {
    const modal = new bootstrap.Modal(document.getElementById('modalNuevaConsulta'));
    modal.show();
}

function verExpedienteCompleto(btn) {
    window.location.href = btn.dataset.url;
}

function imprimirExpediente() {
    window.print();
}


// ===============================
// DETALLE CONSULTA (DEMO)
// ===============================
function verConsultaDetalle(consultaId) {
    Swal.fire({
        title: 'Cargando detalles...',
        html: 'Obteniendo información de la consulta',
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading()
    });

    setTimeout(() => {
        Swal.fire({
            title: 'Detalle de Consulta',
            html: `
                <div class="text-start">
                    <p><strong>ID:</strong> ${consultaId}</p>
                    <p><strong>Paciente:</strong> ${pacienteNombre}</p>
                    <p class="mt-3">Aquí luego mostraremos toda la información clínica.</p>
                </div>
            `,
            icon: 'info',
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#10B981'
        });
    }, 800);
}


// ===============================
// VALIDAR FECHA Y HORA CLÍNICA
// ===============================
function validarFechaHora(input){

    if(!input.value) return true;

    const fechaHora = new Date(input.value);
    const ahora = new Date();

    ahora.setSeconds(0,0);

    // ❌ fechas pasadas
    if(fechaHora.getTime() < ahora.getTime()){
        Swal.fire(
            'Fecha inválida',
            'No se permiten fechas u horas anteriores al momento actual',
            'warning'
        );
        input.value = "";
        return false;
    }

    const hora = fechaHora.getHours();

    // ❌ fuera horario
    if(hora < 6 || hora >= 16){
        Swal.fire(
            'Fuera de horario',
            'Horario de atención: 6:00 AM a 4:00 PM',
            'warning'
        );
        input.value = "";
        return false;
    }

    return true;
}


// ===============================
// AL CARGAR EL EXPEDIENTE
// ===============================
document.addEventListener('DOMContentLoaded', function() {

    console.log("Expediente cargado para:", pacienteNombre);

    // Campo de próxima cita
    const fechaConsulta = document.getElementById('fechaConsulta');

    if(fechaConsulta){

        // bloquear fechas pasadas
        const ahora = new Date();
        ahora.setSeconds(0,0);
        fechaConsulta.min = ahora.toISOString().slice(0,16);

        fechaConsulta.addEventListener('change', ()=> validarFechaHora(fechaConsulta));
        fechaConsulta.addEventListener('blur', ()=> validarFechaHora(fechaConsulta));
        fechaConsulta.addEventListener('input', ()=> validarFechaHora(fechaConsulta));
    }

    // Primera consulta automática
    if (totalConsultas === 0 && embarazoId !== 0) {
        setTimeout(() => {
            Swal.fire({
                title: 'Primera Consulta Prenatal',
                html: `
                    <div class="text-center">
                        <i class="fas fa-baby-carriage" style="font-size: 3rem; color: #10B981;"></i>
                        <p class="mt-3">${pacienteNombre} está embarazada pero no tiene consultas registradas.</p>
                        <p>¿Desea registrar la primera consulta de control prenatal?</p>
                    </div>
                `,
                icon: 'info',
                showCancelButton: true,
                confirmButtonColor: '#10B981',
                cancelButtonColor: '#6c757d',
                confirmButtonText: '<i class="fas fa-stethoscope"></i> Registrar',
                cancelButtonText: 'Más tarde'
            }).then((result) => {
                if (result.isConfirmed) nuevaConsulta();
            });
        }, 900);
    }

});