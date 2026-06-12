import re
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from parking.models import Parqueadero
from ..forms import RegistroSaaSForm
from ..models import Usuario, EmpresaSaaS, Parqueadero

def login_view(request):
    if request.method == 'POST':
        # Captura directa de datos planos del HTML
        login_input = request.POST.get('login_input', '').strip()
        password_input = request.POST.get('password', '')

        if not login_input or not password_input:
            messages.error(request, "Por favor diligencie todos los campos.")
            return render(request, 'parking/usuarios/login.html')

        # LÓGICA DUAL: ¿Es un correo o un nombre de usuario?
        username_para_auth = login_input
        
        if '@' in login_input:
            # Si contiene un @, buscamos el username real asociado a ese correo
            usuario_encontrado = Usuario.objects.filter(email=login_input).first()
            if usuario_encontrado:
                username_para_auth = usuario_encontrado.username
            else:
                # Si el correo no existe, forzamos un valor inválido para que falle la auth de forma segura
                username_para_auth = None 

        # Autenticación nativa de Django usando el username resuelto
        user = authenticate(request, username=username_para_auth, password=password_input)

        if user is not None:
            if user.is_active:
                login(request, user)
                print(f"-> [OK] Sesión iniciada para: {user.username}. Redirigiendo a Paso 1...")
                # Saltamos obligatoriamente a la selección de sucursal
                return redirect('seleccionar_sucursal') 
            else:
                messages.error(request, "Esta cuenta se encuentra deshabilitada.")
        else:
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
        # Recibir y sanitizar espacios básicos en los extremos
        username_input = request.POST.get('username', '').strip()
        email_input = request.POST.get('email', '').strip()
        password_input = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        nombre_empresa_input = request.POST.get('nombre_empresa', '').strip()

        # --- CAPA DE SEGURIDAD EXTRALIMITADA BACKEND ---
        if " " in username_input or not username_input:
            messages.error(request, "Nombre de usuario inválido.")
            return render(request, 'parking/usuarios/registro.html')

        if password_input != password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'parking/usuarios/registro.html')

        # Verificación doble de formato de correo
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_input):
            messages.error(request, "Formato de correo electrónico no permitido.")
            return render(request, 'parking/usuarios/registro.html')

        # Verificar unicidad en base de datos antes de guardar
        if Usuario.objects.filter(username=username_input).exists():
            messages.error(request, "Este nombre de usuario ya está en uso.")
            return render(request, 'parking/usuarios/registro.html')

        if Usuario.objects.filter(email=email_input).exists():
            messages.error(request, "Este correo electrónico ya está registrado.")
            return render(request, 'parking/usuarios/registro.html')

        try:
            # Creación segura con ORM (Inyección SQL Mitigada de fábrica)
            nueva_empresa = EmpresaSaaS.objects.create(
                nombre_comercial=nombre_empresa_input,
                nit= f"TEMP-{uuid.uuid4().hex[:8].upper()}",
                activo=True
            )
            
            # Creación automática de la sucursal por defecto
            Parqueadero.objects.create(
                nombre_sucursal="Sucursal Principal", 
                empresa=nueva_empresa
            )

            # Instanciar el usuario y Hashear la contraseña obligatoriamente
            nuevo_usuario = Usuario(
                username=username_input,
                email=email_input,
                empresa=nueva_empresa,
                rol='ADMIN'
            )
            nuevo_usuario.set_password(password_input) # Encriptado PBKDF2 nativo
            nuevo_usuario.save()

            messages.success(request, "¡Registro exitoso! Por favor inicia sesión.")
            return redirect('login') # Redirección limpia al Login de tu app

        except Exception as e:
            messages.error(request, f"Ocurrió un error en el servidor de base de datos: {e}")
            return render(request, 'parking/usuarios/registro.html')

    return render(request, 'parking/usuarios/registro.html')