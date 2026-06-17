import re
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from axes.helpers import get_client_ip_address
import axes.attempts as axes_attempts
from django.http import JsonResponse

from parking.models import Parqueadero
from ..forms import RegistroSaaSForm
from ..models import Usuario, EmpresaSaaS, Parqueadero, RegistroAcceso

def _get_client_ip(request):
    """Obtiene la IP real del cliente."""
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

def login_view(request):
    if request.method == 'POST':
        login_input = request.POST.get('login_input', '').strip()
        password_input = request.POST.get('password', '')
        ip = _get_client_ip(request)

        if not login_input or not password_input:
            messages.error(request, "Por favor diligencie todos los campos.")
            return render(request, 'parking/usuarios/login.html')

        # Resolver username desde email si aplica
        username_para_auth = login_input
        if '@' in login_input:
            usuario_encontrado = Usuario.objects.filter(email=login_input).first()
            username_para_auth = usuario_encontrado.username if usuario_encontrado else None

        # Intentar autenticación
        user = None
        if username_para_auth:
            user = authenticate(request, username=username_para_auth, password=password_input)

        if user is not None and user.is_active:
            login(request, user)

            # Registrar acceso exitoso
            RegistroAcceso.objects.create(
                usuario_texto=login_input,
                ip=ip,
                resultado='EXITOSO',
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            return redirect('seleccionar_sucursal')

        elif user is not None and not user.is_active:
            messages.error(request, "Esta cuenta se encuentra deshabilitada.")
            RegistroAcceso.objects.create(
                usuario_texto=login_input,
                ip=ip,
                resultado='FALLIDO',
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

        else:
            # Contar intentos fallidos para este usuario/IP
            from axes.models import AccessAttempt
            ip = _get_client_ip(request)
            intentos = AccessAttempt.objects.filter(
                ip_address=ip
            ).first()

            resultado = 'BLOQUEADO' if (intentos and intentos.failures_since_start >= 5) else 'FALLIDO'
            
            # Login fallido
            RegistroAcceso.objects.create(
                usuario_texto=login_input,
                ip=ip,
                resultado=resultado,
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            messages.error(request, "Usuario, correo o contraseña incorrectos.")

    return render(request, 'parking/usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def seleccionar_sucursal_view(request):
    # Filtramos las sucursales que pertenecen a la empresa asignada al usuario
    sucursales_disponibles = request.user.empresa.sucursales.all()

    if request.method == 'POST':
        sucursal_id = request.POST.get('sucursal_id')
        
        # Validación de seguridad perimetral
        if sucursal_id and sucursales_disponibles.filter(id=sucursal_id).exists():
            # Guardamos la sucursal activa en la sesión del navegador
            request.session['sucursal_activa_id'] = int(sucursal_id)
            print(f"-> [OK] Sucursal activa fijada: {sucursal_id}. Entrando al Dashboard.")
            return redirect('dashboard_resumen_general')
        else:
            messages.error(request, "Selección de sucursal inválida o no autorizada.")

    return render(request, 'parking/usuarios/seleccionar_sucursal.html', {
        'sucursales': sucursales_disponibles
    })

def registro_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username', '').strip()
        email_input    = request.POST.get('email', '').strip()
        password_input = request.POST.get('password', '')
        password_confirm   = request.POST.get('password_confirm', '')
        nombre_empresa_input = request.POST.get('nombre_empresa', '').strip()

        # Validaciones básicas
        if " " in username_input or not username_input:
            messages.error(request, "Nombre de usuario inválido.")
            return render(request, 'parking/usuarios/registro.html')

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_input):
            messages.error(request, "Formato de correo electrónico no permitido.")
            return render(request, 'parking/usuarios/registro.html')

        if password_input != password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'parking/usuarios/registro.html')

        # Validación de fortaleza de contraseña (Django nativo)
        try:
            validate_password(password_input)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'parking/usuarios/registro.html')

        # Unicidad
        if Usuario.objects.filter(username=username_input).exists():
            messages.error(request, "Este nombre de usuario ya está en uso.")
            return render(request, 'parking/usuarios/registro.html')

        if Usuario.objects.filter(email=email_input).exists():
            messages.error(request, "Este correo electrónico ya está registrado.")
            return render(request, 'parking/usuarios/registro.html')

        if not nombre_empresa_input:
            messages.error(request, "El nombre comercial es obligatorio.")
            return render(request, 'parking/usuarios/registro.html')

        try:
            nueva_empresa = EmpresaSaaS.objects.create(
                nombre_comercial=nombre_empresa_input,
                nit='',         # Se llenará en onboarding posterior
                activo=True
            )

            Parqueadero.objects.create(
                nombre_sucursal="Sucursal Principal",
                empresa=nueva_empresa
            )

            nuevo_usuario = Usuario(
                username=username_input,
                email=email_input,
                empresa=nueva_empresa,
                rol='ADMIN',
                is_active=True,  # Cambiar a False cuando actives verificación por email
            )
            nuevo_usuario.set_password(password_input)
            nuevo_usuario.save()

            messages.success(request, "¡Registro exitoso! Por favor inicia sesión.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Ocurrió un error: {e}")
            return render(request, 'parking/usuarios/registro.html')

    return render(request, 'parking/usuarios/registro.html')

def validar_username(request):
    username = request.GET.get('username', '').strip()
    existe = Usuario.objects.filter(username=username).exists()
    return JsonResponse({'disponible': not existe})

def validar_email(request):
    email = request.GET.get('email', '').strip()
    existe = Usuario.objects.filter(email=email).exists()
    return JsonResponse({'disponible': not existe})

def lockout_view(request, credentials, *args, **kwargs):
    return render(request, 'parking/usuarios/lockout.html', status=403)