console.log('✅ editar_usuario.js cargado correctamente');

let editarModal = null;
let modalInicializado = false;

function inicializarModal() {
    if (modalInicializado) return;

    const modalElement = document.getElementById('editarModal');
    const form = document.getElementById('editarForm');

    if (!modalElement || !form) {
        console.error('❌ Modal o formulario no encontrado');
        return;
    }

    editarModal = new bootstrap.Modal(modalElement);

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        guardarCambios();
    });

    modalInicializado = true;
    console.log('✅ Modal inicializado correctamente');
}

window.abrirModal = function (userId) {
    if (!modalInicializado) {
        inicializarModal();
    }

    fetch(`/usuarios/editar/${userId}/`)
        .then(res => {
            if (!res.ok) throw new Error('Error al cargar usuario');
            return res.json();
        })
        .then(data => {
            document.getElementById('userId').value = userId;
            document.getElementById('username').value = data.username;
            document.getElementById('password').value = '';
            editarModal.show();
        })
        .catch(err => {
            console.error(err);
            alert('❌ No se pudo cargar el editor');
        });
};

function guardarCambios() {
    const userId = document.getElementById('userId').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/usuarios/editar/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            username: username,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            editarModal.hide();
            location.reload();
        }
    })
    .catch(err => {
        console.error(err);
        alert('❌ Error al guardar cambios');
    });
}

document.addEventListener('DOMContentLoaded', inicializarModal);
