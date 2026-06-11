document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("formRegistro");
    const username = document.getElementById("id_username");
    const email = document.getElementById("id_email");
    const nombreEmpresa = document.getElementById("id_nombre_empresa");
    const password = document.getElementById("id_password");
    const passwordConfirm = document.getElementById("id_password_confirm");
    const btnSubmit = document.getElementById("btnSubmit");

    // Expresiones regulares de validación
    const usernameRegex = /^[a-zA-Z0-9_.-]+$/;
    const emailRegex = /^[\w\.-]+@[\w\.-]+\.\w+$/;

    function mostrarError(input, divError, mensaje) {
        input.classList.remove("is-valid-custom");
        input.classList.add("is-invalid-custom");
        divError.textContent = mensaje;
        divError.style.display = "block";
    }

    function borrarError(input, divError) {
        input.classList.remove("is-invalid-custom");
        input.classList.add("is-valid-custom");
        divError.textContent = "";
        divError.style.display = "none";
    }

    // 1. Validación Username 
    username.addEventListener("input", function () {
        const errorDiv = document.getElementById("error_username");
        if (username.value.includes(" ")) {
            username.value = username.value.replace(/\s/g, ""); // Borra el espacio inmediatamente
            mostrarError(username, errorDiv, "⚠️ No se permiten espacios en el nombre de usuario.");
        } else if (username.value.trim() === "") {
            mostrarError(username, errorDiv, "El nombre de usuario es obligatorio.");
        } else if (!usernameRegex.test(username.value)) {
            mostrarError(username, errorDiv, "Solo letras, números, guiones o puntos.");
        } else {
            borrarError(username, errorDiv);
        }
        validarFormularioCompleto();
    });

    // 2. Validación Correo 
    email.addEventListener("input", function () {
        const errorDiv = document.getElementById("error_email");
        if (!emailRegex.test(email.value)) {
            mostrarError(email, errorDiv, "⚠️ Introduce un formato de correo válido (ejemplo@correo.com).");
        } else {
            borrarError(email, errorDiv);
        }
        validarFormularioCompleto();
    });

    // 3. Validación Nombre Comercial 
    nombreEmpresa.addEventListener("input", function () {
        const errorDiv = document.getElementById("error_nombre_empresa");
        if (nombreEmpresa.value.trim() === "") {
            mostrarError(nombreEmpresa, errorDiv, "El nombre comercial es requerido.");
        } else {
            borrarError(nombreEmpresa, errorDiv);
        }
        validarFormularioCompleto();
    });

    // 4. Validaciones de Contraseñas
    password.addEventListener("input", function () {
        const errorDiv = document.getElementById("error_password");
        if (password.value.length < 4) {
            mostrarError(password, errorDiv, "La contraseña debe tener al menos 4 caracteres.");
        } else {
            borrarError(password, errorDiv);
        }
        verificarCoincidenciaClaves();
    });

    passwordConfirm.addEventListener("input", function () {
        verificarCoincidenciaClaves();
    });

    function verificarCoincidenciaClaves() {
        const errorDiv = document.getElementById("error_password_confirm");
        if (password.value !== passwordConfirm.value) {
            mostrarError(passwordConfirm, errorDiv, "⚠️ Las contraseñas no coinciden.");
        } else if (passwordConfirm.value === "") {
            mostrarError(passwordConfirm, errorDiv, "Debes confirmar tu contraseña.");
        } else {
            borrarError(passwordConfirm, errorDiv);
        }
        validarFormularioCompleto();
    }

    // Activa o desactiva el botón principal
    function validarFormularioCompleto() {
        const todosValidos = form.querySelectorAll(".is-valid-custom").length === 5;
        btnSubmit.disabled = !todosValidos;
    }
});

// Función global para los ojitos
function togglePasswordVisibility(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector("i");
    
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");
    } else {
        input.type = "password";
        icon.classList.remove("bi-eye");
        icon.classList.add("bi-eye-slash");
    }
}

/// fUNCION PARA LAS RECTAS
document.addEventListener("DOMContentLoaded", function () {
    const enlaceCambioPantalla = document.querySelector(".login-link, [href*='login'], [href*='registro']");

    if (enlaceCambioPantalla) {
        enlaceCambioPantalla.addEventListener("click", function (event) {
            event.preventDefault();
            
            const rutaDestino = this.getAttribute("href");
            const rectasIzquierdas = document.querySelectorAll(".recta-izq");
            const rectasDerechas = document.querySelectorAll(".recta-der");
            const avatar = document.getElementById("avatarAnimado3D");

            if (avatar) {
                avatar.classList.add("reversa-avatar");
            }

            rectasIzquierdas.forEach(linea => {
                linea.classList.add("reversa-izquierda");
            });

            rectasDerechas.forEach(linea => {
                linea.classList.add("reversa-derecha");
            });

            setTimeout(() => {
                window.location.href = rutaDestino;
            }, 700);
        });
    }
});