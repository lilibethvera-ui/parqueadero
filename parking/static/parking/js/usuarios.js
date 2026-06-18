// =======================================================
// registro.js — Lógica para login y registro
// =======================================================

// ============ UTILIDAD: MOSTRAR/OCULTAR CONTRASEÑA ============
// Usada tanto en login.html como en registro.html
function togglePasswordVisibility(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon  = btn.querySelector('i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('bi-eye-slash', 'bi-eye');
    } else {
        input.type = 'password';
        icon.classList.replace('bi-eye', 'bi-eye-slash');
    }
}

// =======================================================
// Todo lo de abajo solo aplica si estamos en registro
// =======================================================
document.addEventListener('DOMContentLoaded', function () {

    // Si no existe el formulario de registro, salimos
    const formRegistro = document.getElementById('formRegistro');
    if (!formRegistro) return;

    // ============ UTILIDADES ============
    function setFieldState(inputId, iconId, fbId, state, message) {
        const input = document.getElementById(inputId);
        const icon  = iconId ? document.getElementById(iconId) : null;
        const fb    = document.getElementById(fbId);

        if (!input || !fb) return;

        input.classList.remove('field-ok', 'field-error', 'field-checking');
        if (icon) icon.className = 'field-icon';

        if (state === 'ok') {
            input.classList.add('field-ok');
            if (icon) icon.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>';
            fb.innerHTML = message
                ? `<span class="text-success small">${message}</span>`
                : '';

        } else if (state === 'error') {
            input.classList.add('field-error');
            if (icon) icon.innerHTML = '<i class="bi bi-x-circle-fill text-danger"></i>';
            fb.innerHTML = `<span class="text-danger small">${message}</span>`;

        } else if (state === 'checking') {
            input.classList.add('field-checking');
            if (icon) icon.innerHTML = '<span class="spinner-border spinner-border-sm text-secondary"></span>';
            fb.innerHTML = `<span class="text-muted small">${message}</span>`;

        } else {
            fb.innerHTML = '';
        }
    }

    // ============ DEBOUNCE ============
    function debounce(fn, delay) {
        let timer;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }

    // ============ VALIDACIÓN USERNAME ============
    const checkUsername = debounce(async function () {
        const val = document.getElementById('id_username').value.trim();

        if (!val) {
            setFieldState('id_username', 'icon_username', 'fb_username',
                'error', 'El nombre de usuario es obligatorio.');
            validarBoton(); return;
        }
        if (/\s/.test(val)) {
            setFieldState('id_username', 'icon_username', 'fb_username',
                'error', 'No se permiten espacios.');
            validarBoton(); return;
        }
        if (!/^[a-zA-Z0-9_.\-]+$/.test(val)) {
            setFieldState('id_username', 'icon_username', 'fb_username',
                'error', 'Solo letras, números, guiones o puntos.');
            validarBoton(); return;
        }

        setFieldState('id_username', 'icon_username', 'fb_username',
            'checking', 'Verificando disponibilidad...');

        try {
            const res  = await fetch(`/validar-username/?username=${encodeURIComponent(val)}`);
            const data = await res.json();
            if (data.disponible) {
                setFieldState('id_username', 'icon_username', 'fb_username',
                    'ok', '¡Nombre de usuario disponible!');
            } else {
                setFieldState('id_username', 'icon_username', 'fb_username',
                    'error', 'Este nombre de usuario ya está en uso.');
            }
        } catch {
            setFieldState('id_username', 'icon_username', 'fb_username',
                'error', 'Error al verificar. Intenta de nuevo.');
        }
        validarBoton();
    }, 500);

    document.getElementById('id_username')
        .addEventListener('input', checkUsername);

    // ============ VALIDACIÓN EMAIL ============
    const checkEmail = debounce(async function () {
        const val = document.getElementById('id_email').value.trim();
        const emailRegex = /^[\w\.-]+@[\w\.-]+\.\w+$/;

        if (!val) {
            setFieldState('id_email', 'icon_email', 'fb_email',
                'error', 'El correo es obligatorio.');
            validarBoton(); return;
        }
        if (!emailRegex.test(val)) {
            setFieldState('id_email', 'icon_email', 'fb_email',
                'error', 'Formato inválido (ejemplo@correo.com).');
            validarBoton(); return;
        }

        setFieldState('id_email', 'icon_email', 'fb_email',
            'checking', 'Verificando correo...');

        try {
            const res  = await fetch(`/validar-email/?email=${encodeURIComponent(val)}`);
            const data = await res.json();
            if (data.disponible) {
                setFieldState('id_email', 'icon_email', 'fb_email',
                    'ok', 'Correo disponible.');
            } else {
                setFieldState('id_email', 'icon_email', 'fb_email',
                    'error', 'Este correo ya está registrado.');
            }
        } catch {
            setFieldState('id_email', 'icon_email', 'fb_email',
                'error', 'Error al verificar. Intenta de nuevo.');
        }
        validarBoton();
    }, 500);

    document.getElementById('id_email')
        .addEventListener('input', checkEmail);

    // ============ VALIDACIÓN NOMBRE EMPRESA ============
    document.getElementById('id_nombre_empresa')
        .addEventListener('input', function () {
            const val = this.value.trim();
            if (!val) {
                setFieldState('id_nombre_empresa', 'icon_empresa', 'fb_empresa',
                    'error', 'El nombre comercial es obligatorio.');
            } else {
                setFieldState('id_nombre_empresa', 'icon_empresa', 'fb_empresa',
                    'ok', '');
            }
            validarBoton();
        });

    // ============ BARRA DE FORTALEZA + CHECKLIST ============
    function evaluarPassword(val) {
        const reqs = {
            len:        val.length >= 8,
            upper:      /[A-Z]/.test(val),
            num:        /[0-9]/.test(val),
            notonlynum: !/^\d+$/.test(val),
        };

        // Actualizar cada ítem del checklist
        Object.entries(reqs).forEach(([key, ok]) => {
            const li   = document.getElementById(`req_${key}`);
            if (!li) return;
            const icon = li.querySelector('i');
            if (ok) {
                li.classList.add('req-ok');
                li.classList.remove('req-fail');
                icon.className = 'bi bi-check-circle-fill';
            } else {
                li.classList.add('req-fail');
                li.classList.remove('req-ok');
                icon.className = 'bi bi-x-circle-fill';
            }
        });

        // Calcular nivel y actualizar barra
        const passed = Object.values(reqs).filter(Boolean).length;
        const bar    = document.getElementById('strengthBar');
        if (bar) {
            bar.className = 'strength-bar';
            if (!val) {
                bar.style.width = '0';
            } else if (passed <= 1) {
                bar.classList.add('strength-weak');
                bar.style.width = '25%';
            } else if (passed === 2) {
                bar.classList.add('strength-fair');
                bar.style.width = '50%';
            } else if (passed === 3) {
                bar.classList.add('strength-good');
                bar.style.width = '75%';
            } else {
                bar.classList.add('strength-strong');
                bar.style.width = '100%';
            }
        }

        return Object.values(reqs).every(Boolean);
    }

    // ============ VALIDACIÓN CONTRASEÑA ============
    document.getElementById('id_password')
        .addEventListener('input', function () {
            const val   = this.value;
            const valid = evaluarPassword(val);

            if (!val) {
                setFieldState('id_password', null, 'fb_password',
                    'error', 'La contraseña es obligatoria.');
            } else if (!valid) {
                setFieldState('id_password', null, 'fb_password',
                    'error', 'La contraseña no cumple todos los requisitos.');
            } else {
                setFieldState('id_password', null, 'fb_password',
                    'ok', '¡Contraseña segura!');
            }

            // Re-validar confirmación si ya tiene algo escrito
            const confirmInput = document.getElementById('id_password_confirm');
            if (confirmInput && confirmInput.value) {
                validarConfirmacion();
            }
            validarBoton();
        });

    // ============ VALIDACIÓN CONFIRMACIÓN ============
    function validarConfirmacion() {
        const p1 = document.getElementById('id_password').value;
        const p2 = document.getElementById('id_password_confirm').value;

        if (!p2) {
            setFieldState('id_password_confirm', null, 'fb_confirm',
                'error', 'Confirma tu contraseña.');
        } else if (p1 !== p2) {
            setFieldState('id_password_confirm', null, 'fb_confirm',
                'error', 'Las contraseñas no coinciden.');
        } else {
            setFieldState('id_password_confirm', null, 'fb_confirm',
                'ok', '¡Las contraseñas coinciden!');
        }
        validarBoton();
    }

    document.getElementById('id_password_confirm')
        .addEventListener('input', validarConfirmacion);

    // ============ HABILITAR BOTÓN ============
    function validarBoton() {
        const ids = [
            'id_username',
            'id_email',
            'id_nombre_empresa',
            'id_password',
            'id_password_confirm',
        ];
        const todosOk = ids.every(id => {
            const el = document.getElementById(id);
            return el && el.classList.contains('field-ok');
        });
        const btn = document.getElementById('btnSubmit');
        if (btn) btn.disabled = !todosOk;
    }

}); // fin DOMContentLoaded