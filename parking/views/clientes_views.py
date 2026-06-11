from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.db.models import Q, Sum
from ..models import (
    Cliente, 
    Vehiculo,
    Estacionamiento, 
    EmpresaCorporativa, 
    ContactoAutorizado, 
    VehiculoAutorizado,
    ConvenioEmpresa,
    TerminoPagoEmpresa,
)
from ..forms import (
    ClienteForm, 
    VehiculoForm, 
    EmpresaCorporativaForm, 
    ContactoAutorizadoForm,
    VehiculoAutorizadoForm,
    ConvenioEmpresaForm,
    TerminoPagoEmpresaForm,
)

# ========= 5.1 CLIENTES FRECUENTES =========
def clientes_frecuentes_historial(request):
    # Buscador en la lista de clientes
    query = request.GET.get("q", "")
    cliente_id = request.GET.get("cliente_id")

    # 🔹 LISTA DE CLIENTES: TODOS
    clientes = Cliente.objects.all().prefetch_related("vehiculos")

    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(documento__icontains=query) |
            Q(vehiculos__placa__icontains=query)
        ).distinct()

    # 🔹 Datos para el modal
    selected_cliente = None
    estacionamientos = Estacionamiento.objects.none()
    resumen = {}

    if cliente_id:
        selected_cliente = get_object_or_404(Cliente, id=cliente_id)

        estacionamientos = (
            Estacionamiento.objects
            .filter(cliente=selected_cliente)
            .select_related("vehiculo")
        )

        total_visitas = estacionamientos.count()
        total_pagado = estacionamientos.aggregate(
            total=Sum("valor_cobrado")
        )["total"] or 0

        total_minutos = 0
        ultima_visita = None
        for e in estacionamientos:
            if e.duracion_minutos:
                total_minutos += e.duracion_minutos
            if not ultima_visita or e.fecha_hora_entrada > ultima_visita:
                ultima_visita = e.fecha_hora_entrada

        horas = total_minutos // 60
        resto = total_minutos % 60
        if horas and resto:
            total_horas_texto = f"{horas} h {resto} min"
        elif horas:
            total_horas_texto = f"{horas} h"
        else:
            total_horas_texto = f"{resto} min"

        resumen = {
            "total_visitas": total_visitas,
            "total_minutos": total_minutos,
            "total_horas_texto": total_horas_texto,
            "total_pagado": total_pagado,
            "ultima_visita": ultima_visita,
        }

    context = {
        "section_group": "Gestión de Clientes · Clientes Frecuentes",
        "section_title": "Historial de estacionamientos",
        "section_description": (
            "Consulta el historial de estacionamientos de tus clientes registrados."
        ),
        "section_code": "CF-HISTORIAL",
        "active_menu": "clientes",
        "active_submenu": "frecuentes",

        "clientes": clientes,
        "query": query,
        "selected_cliente": selected_cliente,
        "estacionamientos": estacionamientos,
        "resumen": resumen,
    }

    return render(request, "parking/clientes/clientes_frecuentes_historial.html", context)
    
def clientes_frecuentes_listado(request):
    # Formularios base para el modal (crear cliente)
    cliente_form = ClienteForm(
        prefix="nuevo_cliente",
        initial={"tipo": "FRECUENTE"}
    )
    vehiculo_form = VehiculoForm(prefix="nuevo_vehiculo")

    if request.method == "POST":
        action = request.POST.get("action")

        # --------- CREAR DESDE MODAL ---------
        if action == "crear":
            cliente_form = ClienteForm(
                request.POST,
                prefix="nuevo_cliente"
            )
            vehiculo_form = VehiculoForm(
                request.POST,
                prefix="nuevo_vehiculo"
            )

            if cliente_form.is_valid() and vehiculo_form.is_valid():
                cliente = cliente_form.save(commit=False)
                cliente.tipo = "FRECUENTE"
                cliente.save()

                vehiculo = vehiculo_form.save(commit=False)
                vehiculo.cliente = cliente
                vehiculo.save()

                return redirect("clientes_frecuentes_listado")

        # --------- EDITAR INLINE EN LA TABLA ---------
        elif action == "editar":
            cliente_id = request.POST.get("cliente_id")
            try:
                cliente = Cliente.objects.get(
                    id=cliente_id,
                    tipo="FRECUENTE"
                )
            except Cliente.DoesNotExist:
                return redirect("clientes_frecuentes_listado")

            cliente.nombre = request.POST.get("nombre", "").strip()
            cliente.apellidos = request.POST.get("apellidos", "").strip()
            cliente.documento = request.POST.get("documento", "").strip()
            cliente.telefono = request.POST.get("telefono", "").strip()
            cliente.email = request.POST.get("email", "").strip()
            cliente.activo = bool(request.POST.get("activo"))

            cliente.save()

            return redirect("clientes_frecuentes_listado")

    # ---------- LISTADO Y BUSCADOR (GET o POST inválido) ----------
    query = request.GET.get("q", "")

    clientes = Cliente.objects.filter(tipo="FRECUENTE")

    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(documento__icontains=query) |
            Q(vehiculos__placa__icontains=query)
        ).distinct()

    context = {
        "section_group": "Gestión de Clientes · Clientes Frecuentes",
        "section_title": "Clientes frecuentes",
        "section_description": "Administra y edita los clientes frecuentes directamente desde esta vista.",
        "section_code": "CF-LISTADO",
        "active_menu": "clientes",
        "active_submenu": "frecuentes",

        "clientes": clientes,
        "query": query,
        "cliente_form": cliente_form,
        "vehiculo_form": vehiculo_form,
    }

    return render(request, "parking/clientes/clientes_frecuentes_listado.html", context)

# ========= 5.2 CLIENTES CORPORATIVOS =========
def clientes_corporativos_info_empresa(request):
    query = request.GET.get("q", "").strip()

    empresas = EmpresaCorporativa.objects.select_related("contacto").all()

    if query:
        empresas = empresas.filter(
            Q(razon_social__icontains=query) |
            Q(nit__icontains=query) |
            Q(contacto__nombre__icontains=query) |
            Q(contacto__documento__icontains=query)
        )

    # SIEMPRE define form, para que en GET exista
    form = EmpresaCorporativaForm()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "crear":
            form = EmpresaCorporativaForm(request.POST)
            if form.is_valid():
                empresa = form.save(commit=False)
                # switch → ACTIVA / INACTIVA
                empresa.estado = "ACTIVA" if request.POST.get("estado_activo") == "1" else "INACTIVA"
                empresa.save()
                return redirect("clientes_corporativos_info_empresa")

        elif action == "editar":
            empresa = get_object_or_404(EmpresaCorporativa, id=request.POST.get("empresa_id"))

            empresa.razon_social = request.POST.get("razon_social", "")
            empresa.nit = request.POST.get("nit", "")
            empresa.email = request.POST.get("email", "")
            empresa.direccion = request.POST.get("direccion", "")
            empresa.ciudad = request.POST.get("ciudad", "")

            # switch → ACTIVA / INACTIVA
            empresa.estado = "ACTIVA" if request.POST.get("estado_activo") == "1" else "INACTIVA"

            # contacto (puede ser vacío)
            contacto_val = request.POST.get("contacto") or None
            empresa.contacto_id = contacto_val

            empresa.save()
            return redirect("clientes_corporativos_info_empresa")

    context = {
        "section_group": "Gestión de Clientes · Clientes Corporativos",
        "section_title": "Información de empresa",
        "section_description": (
            "Gestiona empresas con convenio: datos legales, contacto principal, "
            "dirección y estado."
        ),
        "section_code": "CC-EMPRESA",
        "active_menu": "clientes",
        "active_submenu": "corporativos",

        "empresas": empresas,
        "form": form,
        "query": query,
    }

    return render(request, "parking/clientes/clientes_corporativos_info_empresa.html", context)

def clientes_corporativos_contactos_autorizados(request):
    query = request.GET.get("q", "")

    contactos = (
        ContactoAutorizado.objects
        .select_related("empresa")
        .all()
    )

    if query:
        contactos = contactos.filter(
            Q(nombre__icontains=query) |
            Q(documento__icontains=query) |
            Q(empresa__razon_social__icontains=query) |
            Q(empresa__nit__icontains=query)
        )

    empresas = EmpresaCorporativa.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")
        # Crear desde modal
        if action == "crear":
            form = ContactoAutorizadoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("clientes_corporativos_contactos_autorizados")

        # Editar inline
        elif action == "editar":
            contacto_id = request.POST.get("contacto_id")
            contacto = get_object_or_404(ContactoAutorizado, id=contacto_id)
            contacto.nombre = request.POST.get("nombre", "").strip()
            contacto.documento = request.POST.get("documento", "").strip()
            contacto.telefono = request.POST.get("telefono", "").strip()
            contacto.email = request.POST.get("email", "").strip()
            contacto.empresa_id = request.POST.get("empresa_id") or contacto.empresa_id
            contacto.activo = "activo" in request.POST
            contacto.save()
            return redirect("clientes_corporativos_contactos_autorizados")

    # GET normal → form vacío para el modal
    form = ContactoAutorizadoForm()

    context = {
        "section_group": "Gestión de Clientes · Clientes Corporativos",
        "section_title": "Contactos autorizados",
        "section_description": (
            "Personas autorizadas por cada empresa para gestionar estacionamientos, "
            "pagos y reportes."
        ),
        "section_code": "CC-CONTACTOS",
        "active_menu": "clientes",
        "active_submenu": "corporativos",
        "contactos": contactos,
        "empresas": empresas,
        "form": form,
        "query": query,
    }

    return render(request, "parking/clientes/clientes_corporativos_contactos_autorizados.html", context)

def clientes_corporativos_vehiculos_registrados(request):
    query = request.GET.get("q", "")

    vehiculos = (
        VehiculoAutorizado.objects
        .select_related("empresa")
        .all()
    )

    if query:
        vehiculos = vehiculos.filter(
            Q(placa__icontains=query) |
            Q(empresa__razon_social__icontains=query) |
            Q(empresa__nit__icontains=query)
        )

    empresas = EmpresaCorporativa.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")
        # Crear desde modal
        if action == "crear":
            data = request.POST.copy()
            # Forzar mayúsculas en placa
            if "placa" in data and data["placa"]:
                data["placa"] = data["placa"].upper()

            form = VehiculoAutorizadoForm(data)
            if form.is_valid():
                form.save()
                return redirect("clientes_corporativos_vehiculos_registrados")
        # Editar inline
        elif action == "editar":
            vehiculo_id = request.POST.get("vehiculo_id")
            veh = get_object_or_404(VehiculoAutorizado, id=vehiculo_id)
            placa = (request.POST.get("placa") or "").strip().upper()
            veh.placa = placa
            veh.tipo_vehiculo = (request.POST.get("tipo_vehiculo") or "").strip()
            veh.descripcion = (request.POST.get("descripcion") or "").strip()
            veh.empresa_id = request.POST.get("empresa_id") or veh.empresa_id
            veh.activo = "activo" in request.POST
            veh.save()
            return redirect("clientes_corporativos_vehiculos_registrados")

    # GET normal → form vacío para modal
    form = VehiculoAutorizadoForm()

    context = {
        "section_group": "Gestión de Clientes · Clientes Corporativos",
        "section_title": "Vehículos autorizados",
        "section_description": (
            "Vehículos que pueden usar el parqueadero bajo convenio con cada empresa."
        ),
        "section_code": "CC-VEHICULOS",
        "active_menu": "clientes",
        "active_submenu": "corporativos",
        "vehiculos": vehiculos,
        "empresas": empresas,
        "form": form,
        "query": query,
    }

    return render(request, "parking/clientes/clientes_corporativos_vehiculos_registrados.html", context)

def clientes_corporativos_terminos_pago(request):
    q = request.GET.get("q", "").strip()

    empresas = EmpresaCorporativa.objects.all().order_by("razon_social")
    if q:
        empresas = empresas.filter(
            Q(razon_social__icontains=q) |
            Q(nit__icontains=q) |
            Q(email__icontains=q) |
            Q(ciudad__icontains=q)
        )

    # para mostrar errores si algo falla
    form_error = None
    empresa_error_id = None

    if request.method == "POST":
        empresa_id = request.POST.get("empresa_id")
        empresa = get_object_or_404(EmpresaCorporativa, id=empresa_id)

        termino, _created = TerminoPagoEmpresa.objects.get_or_create(empresa=empresa)
        form = TerminoPagoEmpresaForm(request.POST, instance=termino)

        if form.is_valid():
            form.save()
            return redirect("clientes_corporativos_terminos_pago")
        else:
            # guardamos el error para mostrarlo en el modal
            form_error = form
            empresa_error_id = empresa.id
            # debug opcional:
            print("POST:", dict(request.POST))
            print("ERRORES:", form.errors)

    # form vacío para modales (si no hay error en ese modal)
    empty_form = TerminoPagoEmpresaForm()

    return render(request, "parking/clientes/clientes_corporativos_terminos_pago.html", {
        "empresas": empresas,
        "query": q,
        "empty_form": empty_form,
        "form_error": form_error,
        "empresa_error_id": empresa_error_id,
    })

# ========= 5.3 PROGRAMAS DE FIDELIDAD =========
def clientes_fidelidad_puntos(request):
    context = {
        "section_group": "Gestión de Clientes · Programas de Fidelidad",
        "section_title": "Puntos por estacionamiento",
        "section_description": (
            "Diseña y controla la forma en que tus clientes acumulan puntos "
            "por cada estacionamiento realizado."
        ),
        "section_code": "PF-PUNTOS",
        "active_menu": "clientes",
        "active_submenu": "fidelidad",
    }
    return render(request, "parking/clientes/clientes_section.html", context)

def clientes_fidelidad_beneficios(request):
    context = {
        "section_group": "Gestión de Clientes · Programas de Fidelidad",
        "section_title": "Beneficios y premios",
        "section_description": (
            "Administra los premios, descuentos y beneficios que los clientes "
            "pueden canjear usando sus puntos."
        ),
        "section_code": "PF-BENEFICIOS",
        "active_menu": "clientes",
        "active_submenu": "fidelidad",
    }
    return render(request, "parking/clientes/clientes_section.html", context)

def clientes_fidelidad_niveles(request):
    context = {
        "section_group": "Gestión de Clientes · Programas de Fidelidad",
        "section_title": "Niveles de membresía",
        "section_description": (
            "Crea niveles (Bronce, Plata, Oro, etc.) con beneficios y requisitos "
            "diferentes según el uso del parqueadero."
        ),
        "section_code": "PF-NIVELES",
        "active_menu": "clientes",
        "active_submenu": "fidelidad",
    }
    return render(request, "parking/clientes/clientes_section.html", context)



