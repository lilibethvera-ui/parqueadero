document.addEventListener('DOMContentLoaded', function () {
    // ================== TOGGLE SIDEBAR (LO QUE YA TENÍAS) ==================
    const toggleBtn = document.getElementById('toggleSidebar');

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            // En escritorio: colapsar sidebar (solo iconos)
            if (window.innerWidth >= 768) {
                document.body.classList.toggle('sidebar-collapsed');
            } else {
                // En móvil: abrir/cerrar sidebar completa
                document.body.classList.toggle('sidebar-open');
            }
        });
    }

    // ================== ROTAR FLECHAS DEL SIDEBAR ==================
    // Aplica tanto al grupo principal (Gestión de Clientes)
    // como a los submenús (Clientes Frecuentes, Corporativos, etc.)
    const collapsibleTriggers = document.querySelectorAll(
        '.sidebar-link[data-bs-toggle="collapse"], ' +
        '.sidebar-sublink-header[data-bs-toggle="collapse"]'
    );

    collapsibleTriggers.forEach((trigger) => {
        const chevron = trigger.querySelector('.bi-chevron-down');
        if (!chevron) return;

        // Detectar el target del collapse (#menuClientes, #submenuClientesFrecuentes, etc.)
        const targetSelector =
            trigger.getAttribute('href') || trigger.getAttribute('data-bs-target');
        const target = targetSelector ? document.querySelector(targetSelector) : null;

        // Estado inicial: si el collapse ya está abierto (tiene .show), rotamos la flecha
        if (target && target.classList.contains('show')) {
            chevron.classList.add('rotated');
        }

        // Escuchamos los eventos de Bootstrap para mantener la flecha en sync
        if (target) {
            target.addEventListener('shown.bs.collapse', function () {
                chevron.classList.add('rotated');
            });

            target.addEventListener('hidden.bs.collapse', function () {
                chevron.classList.remove('rotated');
            });
        }
    });
});
