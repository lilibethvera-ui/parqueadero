import json
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from ..models import (
    TarifaBaseTiempo,
    TarifaBaseDiaria,
    TarifaBaseNocturna,
)
from ..forms import (
    TarifaBaseTiempoForm,
    TarifaBaseDiariaForm,
    TarifaBaseNocturnaForm
)

# ---- FUNCION DE AYUDA ---
def helper_update_field(obj, payload, allowed_fields):
    field = payload.get("field")
    value = payload.get("value")

    if field not in allowed_fields:
        return None, "Campo no permitido"
    
    # Normalizacion de valores
    if value in (None, "", "null"):
        value = None

    try: 
        setattr(obj, field, value)
        obj.save()
        return True, None
    except Exception as e:
        return None, str(e)


@require_http_methods(["GET", "POST"])
def tarifas_base_dia_noche(request):
    # gestion de tarifas diarias y nocturnas
    diarias = TarifaBaseDiaria.objects.all().order_by("tipo_vehiculo", "nombre")
    nocturnas = TarifaBaseNocturna.objects.all().order_by("tipo_vehiculo", "nombre")

    if request.method == "POST":
        kind = request.POST.get("kind")
        if kind == "dia":
            form = TarifaBaseDiariaForm(request.POST, prefix="dia")
        else: 
            form = TarifaBaseNocturnaForm(request.POST, prefix="noche")

        if form.is_valid():
            form.save()
            messages.success(request, f"Tarifa {kind} creada correctamete.")
            return redirect("tarifas_base_dia_noche")
        messages.error(request, "Error en el formulario")

    return render(request, "parking/tarifas/tarifas_base_dia_noche.html", {
        "diarias": diarias,
        "nocturnas": nocturnas,
        "form_diaria": TarifaBaseDiariaForm(prefix="dia"),
        "form_nocturna": TarifaBaseNocturnaForm(prefix="noche"),
    })

@require_http_methods(["POST"])
def tarifa_inline_update(request, model_type, pk):
    """Vista única para actualizaciones rápidas de cualquier tarifa"""
    models_map = {
        'tiempo': TarifaBaseTiempo,
        'diaria': TarifaBaseDiaria,
        'nocturna': TarifaBaseNocturna
    }
    
    model_class = models_map.get(model_type)
    obj = get_object_or_404(model_class, pk=pk)
    
    try:
        payload = json.loads(request.body)
        # Aquí defines qué campos permites editar según el modelo
        success, error = helper_update_field(obj, payload, allowed_fields=["nombre", "precio_hora", "activo", "precio_dia"])
        if success:
            return JsonResponse({"ok": True})
        return HttpResponseBadRequest(error)
    except:
        return HttpResponseBadRequest("Error al procesar")

@require_http_methods(["GET", "POST"])
def tarifa_base_tiempo_list_create(request):
    tarifas = TarifaBaseTiempo.objects.all()
    form = TarifaBaseTiempoForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Tarifa creada.")
            return redirect("tarifas_base_tiempo")
        else:
            messages.error(request, "Revisa los campos del formulario.")

    return render(request, "parking/tarifas/tarifas_base_tiempo.html", {
        "tarifas": tarifas,
        "form": form,
    })

@require_http_methods(["POST"])
def tarifa_base_tiempo_toggle_activo(request, pk):
    obj = get_object_or_404(TarifaBaseTiempo, pk=pk)
    try:
        data = json.loads(request.body.decode("utf-8"))
        activo = bool(data.get("activo"))
    except Exception:
        return HttpResponseBadRequest("JSON inválido")

    obj.activo = activo
    obj.save(update_fields=["activo"])
    return JsonResponse({"ok": True, "activo": obj.activo})

@require_http_methods(["POST"])
def tarifa_base_tiempo_inline_update(request, pk):

    obj = get_object_or_404(TarifaBaseTiempo, pk=pk)

    try:
        data = json.loads(request.body.decode("utf-8"))
        field = data.get("field")
        value = data.get("value")
    except Exception:
        return HttpResponseBadRequest("JSON inválido")

    allowed = {
        "nombre",
        "modo",
        "minimo_minutos",
        "redondeo",
        "precio_hora",
        "tamano_fraccion_min",
        "precio_fraccion",
    }
    if field not in allowed:
        return HttpResponseBadRequest("Campo no permitido")

    # Convertir tipos simples
    int_fields = {"minimo_minutos", "precio_hora", "tamano_fraccion_min", "precio_fraccion"}
    if field in int_fields:
        if value in (None, "", "null"):
            value = None
        else:
            try:
                value = int(value)
            except ValueError:
                return HttpResponseBadRequest("Debe ser un número entero")

    setattr(obj, field, value)

    # Reglas básicas de consistencia según modo
    if field == "modo":
        if obj.modo == TarifaBaseTiempo.Modo.HORA:
            obj.tamano_fraccion_min = None
            obj.precio_fraccion = None
        else:
            obj.precio_hora = None

    # Validación mínima
    if obj.modo == TarifaBaseTiempo.Modo.HORA and obj.precio_hora is None:
        # no forzamos aquí si está editando por partes; pero puedes descomentar si quieres bloquear
        pass

    obj.save()
    return JsonResponse({"ok": True})

def tarifa_base_diaria_list_create(request):
    tarifas = TarifaBaseDiaria.objects.all().order_by("tipo_vehiculo")
    form = TarifaBaseDiariaForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Tarifa diaria creada.")
            return redirect("tarifas_base_diaria")
        else:
            messages.error(request, "Revisa el formulario.")

    return render(request, "parking/tarifas/tarifas_base_diaria.html", {
        "tarifas": tarifas,
        "form": form,
    })


@require_http_methods(["POST"])
def tarifa_base_diaria_inline_update(request, pk):
    obj = get_object_or_404(TarifaBaseDiaria, pk=pk)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("JSON inválido")

    field = payload.get("field")
    value = payload.get("value")

    allowed = {"nombre", "tipo_vehiculo", "modo_diaria", "hora_corte", "precio_dia"}
    if field not in allowed:
        return HttpResponseBadRequest("Campo no permitido")

    # Normalizaciones simples
    if field in {"precio_dia"}:
        value = value if value not in (None, "") else "0"

    if field == "hora_corte":
        # permitir vacío
        value = value or None

    setattr(obj, field, value)
    obj.save(update_fields=[field, "actualizado_en"])
    return JsonResponse({"ok": True})

@require_http_methods(["POST"])
def tarifa_base_diaria_toggle(request, pk):
    obj = get_object_or_404(TarifaBaseDiaria, pk=pk)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("JSON inválido")

    activo = payload.get("activo")
    if activo is None:
        return HttpResponseBadRequest("Falta 'activo'")

    obj.activo = bool(activo)
    obj.save(update_fields=["activo", "actualizado_en"])
    return JsonResponse({"ok": True, "activo": obj.activo})

@require_http_methods(["GET", "POST"])
def tarifas_base_dia_noche(request):
    # listas
    diarias = TarifaBaseDiaria.objects.all().order_by("tipo_vehiculo", "nombre")
    nocturnas = TarifaBaseNocturna.objects.all().order_by("tipo_vehiculo", "nombre")

    # forms (dos modales)
    form_diaria = TarifaBaseDiariaForm(prefix="dia")
    form_nocturna = TarifaBaseNocturnaForm(prefix="noche")

    if request.method == "POST":
        kind = request.POST.get("kind")  # "dia" o "noche"

        if kind == "dia":
            form_diaria = TarifaBaseDiariaForm(request.POST, prefix="dia")
            if form_diaria.is_valid():
                form_diaria.save()
                messages.success(request, "Tarifa diaria creada.")
                return redirect("tarifas_base_dia_noche")
            messages.error(request, "Revisa el formulario de Tarifa diaria.")

        elif kind == "noche":
            form_nocturna = TarifaBaseNocturnaForm(request.POST, prefix="noche")
            if form_nocturna.is_valid():
                form_nocturna.save()
                messages.success(request, "Tarifa nocturna creada.")
                return redirect("tarifas_base_dia_noche")
            messages.error(request, "Revisa el formulario de Tarifa nocturna.")

    return render(request, "parking/tarifas/tarifas_base_dia_noche.html", {
        "diarias": diarias,
        "nocturnas": nocturnas,
        "form_diaria": form_diaria,
        "form_nocturna": form_nocturna,
    })

@require_http_methods(["POST"])
def tarifa_base_nocturna_inline_update(request, pk):
    obj = get_object_or_404(TarifaBaseNocturna, pk=pk)
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("JSON inválido")

    field = data.get("field")
    value = data.get("value")

    allowed = {
        "nombre", "tipo_vehiculo",
        "hora_inicio", "hora_fin",
        "modo", "minimo_minutos", "redondeo",
        "precio_hora", "tamano_fraccion_min", "precio_fraccion",
    }
    if field not in allowed:
        return HttpResponseBadRequest("Campo no permitido")

    # vacíos -> None para decimales/ints
    if field in {"precio_hora", "precio_fraccion"}:
        value = None if value in (None, "", "null") else value
    if field in {"tamano_fraccion_min", "minimo_minutos"}:
        value = None if value in (None, "", "null") else int(value)
    if field in {"hora_inicio", "hora_fin"}:
        value = value or None

    setattr(obj, field, value)

    # consistencia por modo
    if field == "modo":
        if obj.modo == TarifaBaseNocturna.Modo.HORA:
            obj.tamano_fraccion_min = None
            obj.precio_fraccion = None
        else:
            obj.precio_hora = None

    obj.save()
    return JsonResponse({"ok": True})

@require_http_methods(["POST"])
def tarifa_base_nocturna_toggle(request, pk):
    obj = get_object_or_404(TarifaBaseNocturna, pk=pk)
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("JSON inválido")

    if "activo" not in data:
        return HttpResponseBadRequest("Falta 'activo'")

    obj.activo = bool(data.get("activo"))
    obj.save(update_fields=["activo", "actualizado_en"])
    return JsonResponse({"ok": True, "activo": obj.activo})
