// sidebar.js - Control del sidebar y submenús
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');
    const closeBtn = document.querySelector('.sidebar-close-btn');
    const overlay = document.getElementById('sidebarOverlay');
    const submenuToggles = document.querySelectorAll('.submenu-toggle');
    
    // ===== TOGGLE SIDEBAR =====
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            if (window.innerWidth < 992) {
                // MÓVIL/TABLET: Abrir como overlay
                sidebar.classList.add('mobile-open');
                overlay.classList.add('show');
                document.body.style.overflow = 'hidden';
            } else {
                // DESKTOP: Alternar entre colapsado/expandido
                sidebar.classList.toggle('collapsed');
                updateContentMargin();
                
                // Cerrar submenús cuando se colapsa
                if (sidebar.classList.contains('collapsed')) {
                    document.querySelectorAll('.sidebar-submenu.open').forEach(menu => {
                        menu.classList.remove('open');
                    });
                }
            }
        });
    }
    
    // ===== CERRAR SIDEBAR EN MÓVIL =====
    function closeMobileSidebar() {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('show');
        document.body.style.overflow = '';
    }
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeMobileSidebar);
    }
    
    if (overlay) {
        overlay.addEventListener('click', closeMobileSidebar);
    }
    
    // ===== SUBMENÚS =====
    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const submenu = this.closest('.sidebar-submenu');
            const isCurrentlyOpen = submenu.classList.contains('open');
            
            // Si estamos en desktop y sidebar está colapsado, no cerrar otros
            if (window.innerWidth >= 992 && !sidebar.classList.contains('collapsed')) {
                // Cerrar otros submenús abiertos
                document.querySelectorAll('.sidebar-submenu.open').forEach(openMenu => {
                    if (openMenu !== submenu) {
                        openMenu.classList.remove('open');
                    }
                });
            }
            
            // Alternar submenú actual
            submenu.classList.toggle('open');
            
            // Si estamos en móvil, mantener sidebar abierto
            if (window.innerWidth < 992) {
                sidebar.classList.add('mobile-open');
                overlay.classList.add('show');
            }
        });
    });
    
    // ===== ACTUALIZAR MARGEN DEL CONTENIDO =====
    function updateContentMargin() {
        const content = document.querySelector('.content');
        if (!content) return;
        
        if (window.innerWidth < 992) {
            content.style.marginLeft = '0';
        } else if (sidebar.classList.contains('collapsed')) {
            content.style.marginLeft = '70px';
        } else {
            content.style.marginLeft = '250px';
        }
    }
    
    // ===== REDIMENSIONAMIENTO =====
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 992) {
            // En desktop: asegurar que no esté en modo móvil
            sidebar.classList.remove('mobile-open');
            overlay.classList.remove('show');
            document.body.style.overflow = '';
        } else {
            // En móvil: asegurar que no esté colapsado
            sidebar.classList.remove('collapsed');
        }
        updateContentMargin();
    });
    
    // ===== CERRAR AL HACER CLIC FUERA (MÓVIL) =====
    document.addEventListener('click', function(e) {
        if (window.innerWidth < 992 && sidebar.classList.contains('mobile-open')) {
            if (!sidebar.contains(e.target) && e.target !== toggleBtn) {
                closeMobileSidebar();
            }
        }
    });
    
    // ===== INICIALIZAR =====
    updateContentMargin();
    
    // Marcar item activo basado en URL
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-item[href]').forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
            // Abrir submenú padre si existe
            const submenuParent = item.closest('.sidebar-submenu');
            if (submenuParent) {
                submenuParent.classList.add('open');
            }
        }
    });
});