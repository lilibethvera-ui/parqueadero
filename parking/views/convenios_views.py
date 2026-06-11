from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

from ..models import (
	Cliente, 
	EmpresaCorporativa, 
	ConvenioEmpresa, 
	ConvenioVigencia,
	TarifaEspecialConvenio,
	RestriccionHorariaConvenio,
    ConvenioEmpresaLimites,
)	

from ..forms import (
	ConvenioEmpresaForm, 
	ConvenioVigenciaForm, 
	TarifaEspecialConvenioForm,
	RestriccionHorariaConvenioForm,
    ConvenioEmpresaLimitesForm,
)

def convenios_empresas_registrar(request):
    query = request.GET.get("q", "")

    convenios = ConvenioEmpresa.objects.all()

    if query:
        convenios = convenios.filter(
            Q(empresa__icontains=query) |
            Q(nit__icontains=query) |
            Q(email__icontains=query)
        )

    if request.method == "POST":
        action = request.POST.get("action")
        # Crear desde modal
        if action == "crear":
            form = ConvenioEmpresaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("convenios_empresas_registrar")
        # Editar inline
        elif action == "editar":
            convenio_id = request.POST.get("convenio_id")
            convenio = get_object_or_404(ConvenioEmpresa, id=convenio_id)
            convenio.empresa = (request.POST.get("empresa") or "").strip()
            convenio.nit = (request.POST.get("nit") or "").strip()
            convenio.direccion = (request.POST.get("direccion") or "").strip()
            convenio.telefono = (request.POST.get("telefono") or "").strip()
            convenio.email = (request.POST.get("email") or "").strip()
            convenio.activo = "activo" in request.POST
            convenio.save()

            return redirect("convenios_empresas_registrar")

    # GET normal → form vacío para modal
    form = ConvenioEmpresaForm()

    context = {
        "section_group": "Gestión de Convenios · Empresas Convenio",
        "section_title": "Empresas en convenio",
        "section_description": (
            "Registra empresas aliadas (gimnasios, tiendas, etc.) con las que tienes "
            "acuerdos para ofrecer beneficios a los usuarios."
        ),
        "section_code": "CV-EMPRESAS",
        "active_menu": "convenios",
        "active_submenu": "empresas",
        "convenios": convenios,
        "form": form,
        "query": query,
    }

    return render(request, "parking/convenios/convenios_empresas_registrar.html", context)

def convenios_control_limites_restricciones(request):
    query = request.GET.get("q", "")

    empresas = (
        ConvenioEmpresa.objects
        .prefetch_related("limites")
        .order_by("empresa")
    )

    if query:
        empresas = empresas.filter(
            Q(empresa__icontains=query) |
            Q(nit__icontains=query)
        )

    # POST: guardar límites de una empresa
    if request.method == "POST":
        empresa_id = request.POST.get("empresa_id")
        empresa = get_object_or_404(ConvenioEmpresa, pk=empresa_id)

        limites, _ = ConvenioEmpresaLimites.objects.get_or_create(
            empresa=empresa
        )

        prefix = f"empresa_{empresa.id}"
        form_post = ConvenioEmpresaLimitesForm(
            request.POST,
            instance=limites,
            prefix=prefix
        )

        if form_post.is_valid():
            form_post.save()
            messages.success(
                request,
                f"Límites de convenio actualizados para {empresa.empresa}."
            )
            return redirect("convenios_empresas_limites")
        else:
            messages.error(
                request,
                "Revisa los datos ingresados en el formulario."
            )
    else:
        form_post = None
        empresa_id = None

    # Construir lista (empresa, form) para el template
    items = []
    for e in empresas:
        instance = e.limites.first()
        if instance is None:
            instance = ConvenioEmpresaLimites(empresa=e)

        prefix = f"empresa_{e.id}"

        if form_post is not None and str(e.id) == str(empresa_id):
            form = form_post  # reutilizar el form con errores
        else:
            form = ConvenioEmpresaLimitesForm(
                instance=instance,
                prefix=prefix
            )

        items.append((e, form))

    context = {
        "query": query,
        "items": items,  # lista de tuplas (empresa, form_limites)
    }
    return render(
        request,
        "parking/convenios/convenios_control_limites.html",
        context
    )

def convenios_tarifas_configurar(request):
    query = request.GET.get("q", "")

    tarifas = (
        TarifaEspecialConvenio.objects
        .select_related("empresa_convenio")
        .all()
    )

    if query:
        tarifas = tarifas.filter(
            Q(empresa_convenio__empresa__icontains=query) |
            Q(empresa_convenio__nit__icontains=query) |
            Q(tipo_beneficio__icontains=query)
        )

    empresas_convenio = ConvenioEmpresa.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")

        # Crear desde modal
        if action == "crear":
            form = TarifaEspecialConvenioForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("convenios_tarifas_configurar")

        # Editar inline
        elif action == "editar":
            tarifa_id = request.POST.get("tarifa_id")
            tarifa = get_object_or_404(TarifaEspecialConvenio, id=tarifa_id)

            empresa_id = request.POST.get("empresa_convenio_id")
            if empresa_id:
                tarifa.empresa_convenio_id = empresa_id

            tarifa.tipo_beneficio = request.POST.get("tipo_beneficio", tarifa.tipo_beneficio)
            # valor_beneficio
            valor_beneficio_raw = request.POST.get("valor_beneficio") or "0"
            tarifa.valor_beneficio = valor_beneficio_raw.replace(",", ".")
            # consumo_minimo
            consumo_minimo_raw = request.POST.get("consumo_minimo") or "0"
            tarifa.consumo_minimo = consumo_minimo_raw.replace(",", ".")
            tarifa.aplicacion = request.POST.get("aplicacion", tarifa.aplicacion)
            tarifa.activo = "activo" in request.POST
            tarifa.save()

            return redirect("convenios_tarifas_configurar")

    # GET normal → form vacío para modal
    form = TarifaEspecialConvenioForm()

    context = {
        "section_group": "Gestión de Convenios · Tarifas de Convenio",
        "section_title": "Configurar tarifas especiales",
        "section_description": (
            "Define los beneficios que ofrece cada empresa en convenio: minutos de cortesía, "
            "descuentos porcentuales, valores fijos o tarifas especiales."
        ),
        "section_code": "CV-TARIFAS",
        "active_menu": "convenios",
        # "active_submenu": "tarifas", si tienes submenús separados
        "tarifas": tarifas,
        "empresas_convenio": empresas_convenio,
        "form": form,
        "query": query,
    }

    return render(request, "parking/convenios/convenios_tarifas_configurar.html", context)

def convenios_tarifas_vigencia(request):
    query = request.GET.get("q", "")

    vigencias = (
        ConvenioVigencia.objects
        .select_related("empresa_convenio")
        .all()
    )

    if query:
        vigencias = vigencias.filter(
            Q(empresa_convenio__empresa__icontains=query) |
            Q(empresa_convenio__nit__icontains=query)
        )

    empresas_convenio = ConvenioEmpresa.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")

        # Crear desde modal
        if action == "crear":
            form = ConvenioVigenciaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("convenios_tarifas_vigencia")

        # Editar inline
        elif action == "editar":
            vigencia_id = request.POST.get("vigencia_id")
            vig = get_object_or_404(ConvenioVigencia, id=vigencia_id)

            empresa_id = request.POST.get("empresa_convenio_id")
            if empresa_id:
                vig.empresa_convenio_id = empresa_id

            vig.fecha_inicio = request.POST.get("fecha_inicio") or vig.fecha_inicio
            vig.fecha_fin = request.POST.get("fecha_fin") or vig.fecha_fin
            vig.descripcion = (request.POST.get("descripcion") or "").strip()
            vig.activo = "activo" in request.POST
            vig.save()

            return redirect("convenios_tarifas_vigencia")

    # GET normal → form vacío para modal
    form = ConvenioVigenciaForm()

    context = {
        "section_group": "Gestión de Convenios · Tarifas de Convenio",
        "section_title": "Períodos de vigencia",
        "section_description": (
            "Define las fechas de inicio y fin de los convenios para cada empresa aliada."
        ),
        "section_code": "CV-VIGENCIAS",
        "active_menu": "convenios",
        # si tienes submenús, podrías usar algo tipo: "active_submenu": "tarifas",
        "vigencias": vigencias,
        "empresas_convenio": empresas_convenio,
        "form": form,
        "query": query,
    }

    return render(request, "parking/convenios/convenios_tarifas_vigencia.html", context)

def convenios_control_restricciones_horarias(request):
    """
    - Tabla principal: 1 fila por empresa en convenio.
    - Cada empresa tiene un botón "Configurar horarios" que abre un modal.
    - En el modal se pueden:
        * Agregar varios días de una (checkboxes + hora inicio/fin).
        * Editar día/horas de una fila existente.
        * Eliminar una fila.
    """
    query = request.GET.get("q", "")

    empresas_convenio = (
        ConvenioEmpresa.objects
        .prefetch_related("restricciones_horarias")
        .all()
    )

    if query:
        empresas_convenio = empresas_convenio.filter(
            Q(empresa__icontains=query) |
            Q(nit__icontains=query)
        )

    if request.method == "POST":
        action = request.POST.get("action")
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

        # ===== CREAR HORARIOS =====
        if action == "crear":
            empresa_id = request.POST.get("empresa_convenio")
            hora_inicio = request.POST.get("hora_inicio")
            hora_fin = request.POST.get("hora_fin")
            dias = request.POST.getlist("dias_semana")

            if empresa_id and hora_inicio and hora_fin and dias:
                for d in dias:
                    # 👇 Blindaje extra: no crear si ya existe uno idéntico
                    existe = RestriccionHorariaConvenio.objects.filter(
                        empresa_convenio_id=empresa_id,
                        dia_semana=d,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin,
                    ).exists()

                    if not existe:
                        RestriccionHorariaConvenio.objects.create(
                            empresa_convenio_id=empresa_id,
                            dia_semana=d,
                            hora_inicio=hora_inicio,
                            hora_fin=hora_fin,
                        )

            if is_ajax:
                empresa = ConvenioEmpresa.objects.prefetch_related(
                    "restricciones_horarias"
                ).get(id=empresa_id)
                rows_html = render_to_string(
                    "parking/partials/_convenios_horarios_rows.html",
                    {"empresa": empresa},
                    request=request,
                )
                return JsonResponse({"ok": True, "rows_html": rows_html})

            # submit normal -> recarga la página completa
            return redirect("convenios_control_restricciones_horarias")

        # ===== EDITAR / ELIMINAR HORARIOS =====
        elif action == "editar":
            restriccion_id = request.POST.get("restriccion_id")
            subaction = request.POST.get("subaction", "guardar")

            r = get_object_or_404(RestriccionHorariaConvenio, id=restriccion_id)

            # Eliminar fila
            if subaction == "eliminar":
                r.delete()

                if is_ajax:
                    return JsonResponse({"ok": True})
                return redirect("convenios_control_restricciones_horarias")

            # Guardar cambios
            r.dia_semana = request.POST.get("dia_semana", r.dia_semana)
            r.hora_inicio = request.POST.get("hora_inicio") or r.hora_inicio
            r.hora_fin = request.POST.get("hora_fin") or r.hora_fin
            r.save()

            if is_ajax:
                return JsonResponse({"ok": True})
            return redirect("convenios_control_restricciones_horarias")

    # GET normal → form base para los modales
    form = RestriccionHorariaConvenioForm()

    context = {
        "section_group": "Gestión de Convenios · Control de Acceso",
        "section_title": "Restricciones horarias",
        "section_description": (
            "Define en qué días y horarios pueden utilizarse los convenios de cada empresa aliada."
        ),
        "section_code": "CV-RESTRICCIONES",
        "active_menu": "convenios",
        "empresas_convenio": empresas_convenio,
        "form": form,
        "query": query,
    }

    return render(
        request,
        "parking/convenios/convenios_control_restricciones_horarias.html",
        context,
    )

