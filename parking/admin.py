from django.contrib import admin
from .models import (
    TarifaBaseTiempo, 
    Cliente, 
    Vehiculo, 
    EmpresaCorporativa,
    ConvenioEmpresa,
    RegistroAcceso
)

@admin.register(TarifaBaseTiempo)
class TarifaBaseTiempoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "modo", "activo", "created_at")
    list_filter = ("modo", "activo")
    search_fields = ("nombre",)

class VehiculoInline(admin.TabularInline):
    model = Vehiculo
    extra = 1


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellidos", "documento", "tipo", "telefono", "email", "activo")
    list_filter = ("tipo", "activo")
    search_fields = ("nombre", "apellidos", "documento", "nombre_empresa")
    inlines = [VehiculoInline]


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("placa", "tipo", "cliente", "activo")
    list_filter = ("tipo", "activo")
    search_fields = ("placa", "cliente__nombre", "cliente__apellidos", "cliente__nombre_empresa")

@admin.register(EmpresaCorporativa)
class EmpresaCorporativaAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "nit", "contacto", "estado")
    search_fields = ("razon_social", "nit", "contacto__nombre", "contacto__apellidos")
    list_filter = ("estado",)

# @admin.register(ConvenioEmpresa)
# class ConvenioEmpresaAdmin(admin.ModelAdmin):
#     list_display = ("empresa", "nit", "direccion", "telefono", "email", "activo")
#     search_fields = ("empresa__razon_social", "empresa__nit", "tipo_convenio")
#     list_filter = ("tipo_convenio",)

@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ('usuario_texto', 'resultado', 'ip', 'fecha')
    list_filter = ('resultado',)
    search_fields = ('usuario_texto', 'ip')
    ordering = ('-fecha',)
    readonly_fields = ('usuario_texto', 'ip', 'fecha', 'resultado', 'user_agent')