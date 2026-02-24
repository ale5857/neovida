function confirmarBorrado(event) {
    // Crear ventana modal personalizada
    if (document.getElementById('modal-confirm')) {
        document.getElementById('modal-confirm').remove();
    }
    const modal = document.createElement('div');
    modal.id = 'modal-confirm';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.background = 'rgba(214,51,132,0.18)';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.zIndex = '9999';

    modal.innerHTML = `
        <div style="
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 6px 32px rgba(214,51,132,0.18);
            padding: 32px 28px;
            text-align: center;
            max-width: 350px;
            border: 2px solid #d63384;
        ">
            <div style="font-size: 2.2em; color: #d63384; margin-bottom: 12px;">&#9888;</div>
            <div style="font-size: 1.15em; color: #d63384; margin-bottom: 18px;">
                <strong>¿Está seguro que desea borrar este paciente?</strong><br>
                <span style="color: #6c757d;">Esta acción no se puede deshacer.</span>
            </div>
            <button id="confirm-delete" style="
                background: #ff5c5c;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 10px 22px;
                font-weight: bold;
                margin-right: 10px;
                cursor: pointer;
                box-shadow: 0 2px 8px rgba(255,133,162,0.12);
                transition: background 0.2s;
            ">Sí, borrar</button>
            <button id="cancel-delete" style="
                background: #e9ecef;
                color: #d63384;
                border: none;
                border-radius: 8px;
                padding: 10px 22px;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.2s;
            ">Cancelar</button>
        </div>
    `;
    document.body.appendChild(modal);

    document.getElementById('confirm-delete').onclick = function() {
        modal.remove();
        event.target.onclick = null;
        event.target.click();
    };
    document.getElementById('cancel-delete').onclick = function() {
        modal.remove();
    };
    event.preventDefault();
}