from django.shortcuts import render
from ..models import Cliente, Estacionamiento, Vehiculo

# Vista general (Dashboard principal)
def dashboard_resumen_general(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'vehiculos_activos': Vehiculo.objects.filter(activo=True).count(),
        # 'estacionamientos_disponibles': Estacionamiento.objects.filter(disponible=True).count(),
    }
    return render(request, 'parking/dashboard.html', context)

def inicio(request):
    return dashboard_resumen_general(request)

# ========== RESUMEN GENERAL =============
def dashboard_estado_actual(request):
    context = {
        "section_group": "Resumen General",
        "section_title": "Estado actual del parqueadero",
        "section_description": "Aquí mostraremos el estado actual: capacidad, puestos libres, vehículos dentro, etc."
    }
    return render(request, 'parking/dashboard_section.html', context)

def dashboard_ocupacion_tiempo_real(request):
    context = {
        "section_group": "Resumen General",
        "section_title": "Ocupación en tiempo real",
        "section_description": "Aquí irá un gráfico/tabla con la ocupación en tiempo real del parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def dashboard_ingresos_dia(request):
    context = {
        "section_group": "Resumen General",
        "section_title": "Ingresos del día",
        "section_description": "Aquí se verán los ingresos de hoy, tickets emitidos y comparativo con días anteriores."
    }
    return render(request, 'parking/dashboard_section.html', context)

def dashboard_vehiculos_actuales(request):
    context = {
        "section_group": "Resumen General",
        "section_title": "Vehículos actualmente estacionados",
        "section_description": "Listado y estadísticas de los vehículos que están dentro del parqueadero en este momento."
    }
    return render(request, 'parking/dashboard_section.html', context)

# MÉTRICAS CLAVE 
def dashboard_ingresos_periodos(request):
    context = {
        "section_group": "Métricas Clave",
        "section_title": "Ingresos mensuales / trimestrales",
        "section_description": "Resumen de ingresos agrupados por mes y trimestre."
    }
    return render(request, 'parking/dashboard_section.html', context)

def dashboard_tasa_ocupacion_promedio(request):
    context = {
        "section_group": "Métricas Clave",
        "section_title": "Tasa de ocupación promedio",
        "section_description": "Promedio de ocupación por día, semana y mes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def dashboard_vehiculos_frecuentes(request):
    context = {
        "section_group": "Métricas Clave",
        "section_title": "Vehículos más frecuentes",
        "section_description": "Ranking de clientes/vehículos que más visitan el parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def dashboard_horarios_pico(request):
    context = {
        "section_group": "Métricas Clave",
        "section_title": "Horarios pico",
        "section_description": "Gráficos con los horarios de mayor afluencia."
    }
    return render(request, 'parking/dashboard_section.html', context)

# ================POS - PUNTO DE VENTA===========
# 2.1 REGISTRO DE INGRESOS
def pos_ingresos_entrada(request):
    context = {
        "section_group": "POS - Registro de Ingresos",
        "section_title": "Entrada de vehículos",
        "section_description": "Formulario para registrar la entrada de un vehículo al parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_ingresos_tipo_vehiculo(request):
    context = {
        "section_group": "POS - Registro de Ingresos",
        "section_title": "Selección de tipo de vehículo",
        "section_description": "Pantalla para seleccionar si es carro, moto, camión, bici, etc."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_ingresos_asignar_espacio(request):
    context = {
        "section_group": "POS - Registro de Ingresos",
        "section_title": "Asignación de espacio",
        "section_description": "Asignación automática o manual del espacio de parqueo disponible."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_ingresos_fotografia(request):
    context = {
        "section_group": "POS - Registro de Ingresos",
        "section_title": "Toma de fotografía",
        "section_description": "Captura de imagen de evidencia del vehículo al ingresar."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_ingresos_ticket(request):
    context = {
        "section_group": "POS - Registro de Ingresos",
        "section_title": "Generación de ticket",
        "section_description": "Generación e impresión del ticket de ingreso para el cliente."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 2.2 REGISTRO DE SALIDAS
def pos_salidas_tiempo(request):
    context = {
        "section_group": "POS - Registro de Salidas",
        "section_title": "Cálculo automático de tiempo",
        "section_description": "Cálculo de tiempo de permanencia desde la hora de ingreso hasta la salida."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_salidas_tarifas(request):
    context = {
        "section_group": "POS - Registro de Salidas",
        "section_title": "Aplicación de tarifas",
        "section_description": "Aplicación de la tarifa correspondiente según tipo de vehículo y tiempo."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_salidas_pago_efectivo(request):
    context = {
        "section_group": "POS - Registro de Salidas",
        "section_title": "Pago en efectivo",
        "section_description": "Registro de pagos realizados en efectivo."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_salidas_pago_tarjeta(request):
    context = {
        "section_group": "POS - Registro de Salidas",
        "section_title": "Pago con tarjeta crédito/débito",
        "section_description": "Registro de pagos realizados con tarjeta."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_salidas_pago_transferencia(request):
    context = {
        "section_group": "POS - Registro de Salidas",
        "section_title": "Pago por transferencia",
        "section_description": "Registro de pagos realizados mediante transferencia bancaria."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_salidas_pago_convenios(request):
    context = {
        "section_group": "POS - Registro de Salidas",
        "section_title": "Pago por convenios",
        "section_description": "Pagos asociados a convenios con empresas o clientes frecuentes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_salidas_factura(request):
    context = {
        "section_group": "POS - Registro de Salidas",
        "section_title": "Impresión de factura/comprobante",
        "section_description": "Generación e impresión del comprobante o factura de salida."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 2.3 RESERVAS
def pos_reservas_crear(request):
    context = {
        "section_group": "POS - Reservas",
        "section_title": "Crear reservas",
        "section_description": "Creación de nuevas reservas de espacios de parqueo."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_reservas_modificar(request):
    context = {
        "section_group": "POS - Reservas",
        "section_title": "Modificar reservas",
        "section_description": "Modificación de reservas existentes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_reservas_cancelar(request):
    context = {
        "section_group": "POS - Reservas",
        "section_title": "Cancelar reservas",
        "section_description": "Cancelación de reservas programadas."
    }
    return render(request, 'parking/dashboard_section.html', context)

def pos_reservas_calendario(request):
    context = {
        "section_group": "POS - Reservas",
        "section_title": "Calendario de reservas",
        "section_description": "Visualización en calendario de todas las reservas."
    }
    return render(request, 'parking/dashboard_section.html', context)

# ===============GESTIÓN DE TARIFAS=====================
# Tarifas base
def tarifas_base_hora(request):
    context = {
        "section_group": "Gestión de Tarifas - Tarifas base",
        "section_title": "Tarifa por hora",
        "section_description": "Configuración de la tarifa estándar por hora para el parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def tarifas_base_fracciones(request):
    context = {
        "section_group": "Gestión de Tarifas - Tarifas base",
        "section_title": "Fracciones de hora",
        "section_description": "Definición de tarifas para fracciones de hora (ej. cada 15 o 30 minutos)."
    }
    return render(request, 'parking/dashboard_section.html', context)

def tarifas_base_diaria(request):
    context = {
        "section_group": "Gestión de Tarifas - Tarifas base",
        "section_title": "Tarifa diaria",
        "section_description": "Configuración de tarifa fija para estancias de día completo."
    }
    return render(request, 'parking/dashboard_section.html', context)

def tarifas_base_nocturna(request):
    context = {
        "section_group": "Gestión de Tarifas - Tarifas base",
        "section_title": "Tarifa nocturna",
        "section_description": "Configuración de tarifas especiales para horario nocturno."
    }
    return render(request, 'parking/dashboard_section.html', context)

def tarifas_base_fines_semana(request):
    context = {
        "section_group": "Gestión de Tarifas - Tarifas base",
        "section_title": "Tarifa fines de semana",
        "section_description": "Configuración de tarifas diferenciadas para sábados, domingos y festivos."
    }
    return render(request, 'parking/dashboard_section.html', context)

# Tarifas especiales
def tarifas_especiales_tipo_vehiculo(request):
    context = {
        "section_group": "Gestión de Tarifas - Tarifas especiales",
        "section_title": "Por tipo de vehículo",
        "section_description": "Tarifas específicas según el tipo de vehículo (carros, motos, camiones, etc.)."
    }
    return render(request, 'parking/dashboard_section.html', context)

def tarifas_especiales_promocionales(request):
    context = {
        "section_group": "Gestión de Tarifas - Tarifas especiales",
        "section_title": "Tarifas promocionales",
        "section_description": "Configuración de tarifas con descuento por campañas promocionales."
    }
    return render(request, 'parking/dashboard_section.html', context)

def tarifas_especiales_descuentos_volumen(request):
    context = {
        "section_group": "Gestión de Tarifas - Tarifas especiales",
        "section_title": "Descuentos por volumen",
        "section_description": "Descuentos para clientes que registran múltiples vehículos o visitas frecuentes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def tarifas_especiales_temporada(request):
    context = {
        "section_group": "Gestión de Tarifas - Tarifas especiales",
        "section_title": "Tarifas por temporada",
        "section_description": "Configuración de tarifas para temporadas específicas (alta, baja, vacaciones, etc.)."
    }
    return render(request, 'parking/dashboard_section.html', context)

# Paquetes y planes
def tarifas_paquetes_mensualidad(request):
    context = {
        "section_group": "Gestión de Tarifas - Paquetes y planes",
        "section_title": "Mensualidad",
        "section_description": "Definición de planes de pago mensual para clientes recurrentes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def tarifas_paquetes_corporativos(request):
    context = {
        "section_group": "Gestión de Tarifas - Paquetes y planes",
        "section_title": "Planes corporativos",
        "section_description": "Configuración de acuerdos y planes especiales para empresas."
    }
    return render(request, 'parking/dashboard_section.html', context)

def tarifas_paquetes_promocionales(request):
    context = {
        "section_group": "Gestión de Tarifas - Paquetes y planes",
        "section_title": "Paquetes promocionales",
        "section_description": "Paquetes con precios especiales por tiempo limitado o campañas."
    }
    return render(request, 'parking/dashboard_section.html', context)

# =============4. GESTIÓN DE CONVENIOS===================
# 4.1 Empresas Convenio
def convenios_empresas_registrar(request):
    context = {
        "section_group": "Gestión de Convenios - Empresas Convenio",
        "section_title": "Registrar nueva empresa",
        "section_description": "Formulario para registrar una nueva empresa en el sistema de convenios."
    }
    return render(request, 'parking/dashboard_section.html', context)

def convenios_empresas_limites(request):
    context = {
        "section_group": "Gestión de Convenios - Empresas Convenio",
        "section_title": "Límites y restricciones",
        "section_description": "Configuración de límites y restricciones para cada empresa en convenio."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 4.2 Tarifas de Convenio
def convenios_tarifas_configurar(request):
    context = {
        "section_group": "Gestión de Convenios - Tarifas de Convenio",
        "section_title": "Configurar tarifas especiales",
        "section_description": "Definición de tarifas especiales aplicables a empresas en convenio."
    }
    return render(request, 'parking/dashboard_section.html', context)

def convenios_tarifas_vigencia(request):
    context = {
        "section_group": "Gestión de Convenios - Tarifas de Convenio",
        "section_title": "Períodos de vigencia",
        "section_description": "Definición de fechas de inicio y fin de las tarifas de convenio."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 4.3 Control de Acceso
def convenios_control_restricciones_horarias(request):
    context = {
        "section_group": "Gestión de Convenios - Control de Acceso",
        "section_title": "Restricciones horarias",
        "section_description": "Configuración de horarios permitidos para el uso de convenios."
    }
    return render(request, 'parking/dashboard_section.html', context)

# =========5. GESTIÓN DE CLIENTES =========
# Clientes 
def clientes_frecuentes_registro(request):
    context = {
        "section_group": "Gestión de Clientes - Clientes Frecuentes",
        "section_title": "Registro de información",
        "section_description": "Formulario para registrar y actualizar la información básica de clientes frecuentes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def clientes_frecuentes_historial(request):
    context = {
        "section_group": "Gestión de Clientes · Clientes Frecuentes",
        "section_title": "Historial de estacionamientos",
        "section_description":"Consulta el historial de estacionamientos de tus clientes frecuentes."
    }

    return render(request, "parking/clientes_frecuentes_historial.html", context)

# Clientes Corporativos
def clientes_corporativos_info_empresa(request):
    context = {
        "section_group": "Gestión de Clientes - Clientes Corporativos",
        "section_title": "Información de empresa",
        "section_description": "Registro y edición de la información principal de empresas clientes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def clientes_corporativos_contactos_autorizados(request):
    context = {
        "section_group": "Gestión de Clientes - Clientes Corporativos",
        "section_title": "Contactos autorizados",
        "section_description": "Gestión de las personas autorizadas por la empresa para usar el parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def clientes_corporativos_vehiculos_registrados(request):
    context = {
        "section_group": "Gestión de Clientes - Clientes Corporativos",
        "section_title": "Vehículos registrados",
        "section_description": "Listado y administración de los vehículos asociados a una empresa."
    }
    return render(request, 'parking/dashboard_section.html', context)

def clientes_corporativos_terminos_pago(request):
    context = {
        "section_group": "Gestión de Clientes - Clientes Corporativos",
        "section_title": "Términos de pago",
        "section_description": "Configuración de términos de pago, créditos y condiciones especiales para empresas."
    }
    return render(request, 'parking/dashboard_section.html', context)

# Programas de Fidelidad
def clientes_fidelidad_puntos(request):
    context = {
        "section_group": "Gestión de Clientes - Programas de Fidelidad",
        "section_title": "Puntos por estacionamiento",
        "section_description": "Definición y consulta de puntos acumulados por cada estacionamiento."
    }
    return render(request, 'parking/dashboard_section.html', context)

def clientes_fidelidad_beneficios(request):
    context = {
        "section_group": "Gestión de Clientes - Programas de Fidelidad",
        "section_title": "Beneficios y premios",
        "section_description": "Gestión de beneficios, premios y canjes asociados al programa de fidelidad."
    }
    return render(request, 'parking/dashboard_section.html', context)

def clientes_fidelidad_niveles(request):
    context = {
        "section_group": "Gestión de Clientes - Programas de Fidelidad",
        "section_title": "Niveles de membresía",
        "section_description": "Configuración de niveles (Bronce, Plata, Oro, etc.) y sus ventajas."
    }
    return render(request, 'parking/dashboard_section.html', context)

# ================6. REPORTES Y ANÁLISIS=================
# 6.1 Reportes Financieros
def reportes_financieros_ingresos(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Financieros",
        "section_title": "Ingresos diarios/semanal/mensual",
        "section_description": "Reporte de ingresos agrupados por día, semana y mes para el parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_financieros_flujo_caja(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Financieros",
        "section_title": "Flujo de caja",
        "section_description": "Detalle del flujo de caja, ingresos y egresos asociados a la operación del parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_financieros_comparativos(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Financieros",
        "section_title": "Comparativos periódicos",
        "section_description": "Comparativos de ingresos entre periodos (ej. mes actual vs mes anterior)."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_financieros_tendencias(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Financieros",
        "section_title": "Análisis de tendencias",
        "section_description": "Gráficos y análisis de tendencias financieras a lo largo del tiempo."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 6.2 Reportes Operativos
def reportes_operativos_ocupacion_horarios(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Operativos",
        "section_title": "Ocupación por horarios",
        "section_description": "Reporte de ocupación del parqueadero segmentado por franjas horarias."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_operativos_tipos_vehiculos(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Operativos",
        "section_title": "Tipos de vehículos",
        "section_description": "Distribución de los tipos de vehículos que utilizan el parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_operativos_tiempos_permanencia(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Operativos",
        "section_title": "Tiempos de permanencia",
        "section_description": "Estadísticas de tiempo de permanencia promedio y rangos más frecuentes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_operativos_espacios_mas_utilizados(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Operativos",
        "section_title": "Espacios más utilizados",
        "section_description": "Identificación de los espacios o zonas de parqueo con mayor ocupación."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 6.3 Reportes de Clientes
def reportes_clientes_frecuentes(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes de Clientes",
        "section_title": "Clientes frecuentes",
        "section_description": "Reporte de clientes con mayor recurrencia en el parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_clientes_comportamiento_uso(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes de Clientes",
        "section_title": "Comportamiento de uso",
        "section_description": "Análisis de patrones de uso del parqueadero por parte de los clientes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_clientes_preferencias_pago(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes de Clientes",
        "section_title": "Preferencias de pago",
        "section_description": "Estadísticas de los métodos de pago más utilizados por los clientes."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 6.4 Reportes Personalizados
def reportes_personalizados_filtros(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Personalizados",
        "section_title": "Filtros por fecha/tipo/vehículo",
        "section_description": "Interfaz para generar reportes personalizados aplicando filtros avanzados."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_personalizados_exportacion(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Personalizados",
        "section_title": "Exportación a Excel/PDF",
        "section_description": "Opciones para exportar reportes personalizados a formatos Excel o PDF."
    }
    return render(request, 'parking/dashboard_section.html', context)

def reportes_personalizados_graficos(request):
    context = {
        "section_group": "Reportes y Análisis - Reportes Personalizados",
        "section_title": "Gráficos y estadísticas",
        "section_description": "Visualización gráfica y estadísticas avanzadas de los datos del parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

# =============7. CONFIGURACIÓN DEL SISTEMA=============
# 7.1 Configuración General
def config_sistema_general_datos_negocio(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración General",
        "section_title": "Datos del negocio",
        "section_description": "Configuración de la información básica del negocio (nombre, NIT, dirección, contacto)."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_sistema_general_horarios(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración General",
        "section_title": "Horarios de operación",
        "section_description": "Definición de los horarios de apertura y cierre del parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_sistema_general_impuestos(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración General",
        "section_title": "Impuestos aplicables",
        "section_description": "Configuración de impuestos, tasas y retenciones que aplican a la facturación."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_sistema_general_moneda_formatos(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración General",
        "section_title": "Moneda y formatos",
        "section_description": "Selección de moneda, formato de fecha, hora y demás opciones regionales."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 7.2 Configuración de Espacios
def config_espacios_mapa(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración de Espacios",
        "section_title": "Mapa del parqueadero",
        "section_description": "Diseño y configuración del mapa visual de los espacios de parqueo."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_espacios_tipos(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración de Espacios",
        "section_title": "Tipos de espacios",
        "section_description": "Definición de tipos de espacios (carro, moto, camión, eléctrico, etc.)."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_espacios_zonas(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración de Espacios",
        "section_title": "Asignación de zonas",
        "section_description": "Configuración de zonas o niveles del parqueadero y distribución de espacios."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_espacios_especiales(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración de Espacios",
        "section_title": "Espacios especiales (discapacitados, eléctricos)",
        "section_description": "Gestión de espacios reservados para personas con discapacidad y vehículos eléctricos."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 7.3 Configuración de Dispositivos
def config_dispositivos_impresoras(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración de Dispositivos",
        "section_title": "Impresoras",
        "section_description": "Configuración de impresoras de tickets y facturas conectadas al sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_dispositivos_lectores(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración de Dispositivos",
        "section_title": "Lectores de código de barras",
        "section_description": "Gestión de lectores de código de barras para tickets y tarjetas."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_dispositivos_camaras(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración de Dispositivos",
        "section_title": "Cámaras",
        "section_description": "Configuración de cámaras de vigilancia asociadas al parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_dispositivos_barreras(request):
    context = {
        "section_group": "Configuración del Sistema - Configuración de Dispositivos",
        "section_title": "Barreras de acceso",
        "section_description": "Parámetros de control para barreras de acceso automáticas."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 7.4 Usuarios y Permisos
def config_usuarios_crear(request):
    context = {
        "section_group": "Configuración del Sistema - Usuarios y Permisos",
        "section_title": "Crear usuarios",
        "section_description": "Creación y administración de cuentas de usuarios del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_usuarios_roles_permisos(request):
    context = {
        "section_group": "Configuración del Sistema - Usuarios y Permisos",
        "section_title": "Roles y permisos",
        "section_description": "Definición de roles (operador, supervisor, administrador) y sus permisos."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_usuarios_horarios_acceso(request):
    context = {
        "section_group": "Configuración del Sistema - Usuarios y Permisos",
        "section_title": "Horarios de acceso",
        "section_description": "Control de horarios en los que cada usuario puede acceder al sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def config_usuarios_auditoria(request):
    context = {
        "section_group": "Configuración del Sistema - Usuarios y Permisos",
        "section_title": "Auditoría de actividades",
        "section_description": "Registro y consulta de las acciones realizadas por los usuarios en el sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

# =================8. MÓDULO CONTABLE===================
# 8.1 Cierre de Caja
def contable_cierre_arqueo(request):
    context = {
        "section_group": "Módulo Contable - Cierre de Caja",
        "section_title": "Arqueo de caja",
        "section_description": "Pantalla para realizar el arqueo de caja al cierre de turno o jornada."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_cierre_conciliacion(request):
    context = {
        "section_group": "Módulo Contable - Cierre de Caja",
        "section_title": "Conciliación bancaria",
        "section_description": "Herramientas para conciliar movimientos del sistema con los extractos bancarios."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_cierre_reporte_cierres(request):
    context = {
        "section_group": "Módulo Contable - Cierre de Caja",
        "section_title": "Reporte de cierres",
        "section_description": "Listado y generación de reportes de cierres de caja realizados."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_cierre_historico(request):
    context = {
        "section_group": "Módulo Contable - Cierre de Caja",
        "section_title": "Histórico de cierres",
        "section_description": "Consulta histórica de cierres de caja por fechas, usuarios y turnos."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 8.2 Facturación
def contable_facturacion_emision(request):
    context = {
        "section_group": "Módulo Contable - Facturación",
        "section_title": "Emisión de facturas",
        "section_description": "Emisión de facturas a partir de los movimientos del parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_facturacion_notas_credito(request):
    context = {
        "section_group": "Módulo Contable - Facturación",
        "section_title": "Notas de crédito",
        "section_description": "Gestión de notas de crédito asociadas a facturas emitidas."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_facturacion_control_series(request):
    context = {
        "section_group": "Módulo Contable - Facturación",
        "section_title": "Control de series",
        "section_description": "Control de numeración y series de facturación."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_facturacion_envio_electronico(request):
    context = {
        "section_group": "Módulo Contable - Facturación",
        "section_title": "Envío electrónico",
        "section_description": "Envío electrónico de facturas a clientes y entidades externas."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 8.3 Cuentas por Cobrar
def contable_cxc_estado_cuentas(request):
    context = {
        "section_group": "Módulo Contable - Cuentas por Cobrar",
        "section_title": "Estado de cuentas",
        "section_description": "Resumen de saldos pendientes por cliente y estado de las cuentas por cobrar."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_cxc_cartera_vencida(request):
    context = {
        "section_group": "Módulo Contable - Cuentas por Cobrar",
        "section_title": "Cartera vencida",
        "section_description": "Listado y análisis de cartera vencida por rangos de días."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_cxc_recordatorios_pago(request):
    context = {
        "section_group": "Módulo Contable - Cuentas por Cobrar",
        "section_title": "Recordatorios de pago",
        "section_description": "Gestión de recordatorios de pago enviados a los clientes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_cxc_conciliaciones(request):
    context = {
        "section_group": "Módulo Contable - Cuentas por Cobrar",
        "section_title": "Conciliaciones",
        "section_description": "Conciliación de pagos recibidos contra facturas pendientes."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 8.4 Integraciones Contables
def contable_integraciones_exportacion(request):
    context = {
        "section_group": "Módulo Contable - Integraciones Contables",
        "section_title": "Exportación a sistemas contables",
        "section_description": "Exportación de información del parqueadero a sistemas contables externos."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_integraciones_formatos(request):
    context = {
        "section_group": "Módulo Contable - Integraciones Contables",
        "section_title": "Formatos estándar",
        "section_description": "Configuración de formatos estándar para intercambio de información contable."
    }
    return render(request, 'parking/dashboard_section.html', context)

def contable_integraciones_automatizacion(request):
    context = {
        "section_group": "Módulo Contable - Integraciones Contables",
        "section_title": "Automatización de procesos",
        "section_description": "Automatización de tareas contables recurrentes mediante integraciones."
    }
    return render(request, 'parking/dashboard_section.html', context)

# ================9. SOPORTE Y MANTENIMIENTO===============
# 9.1 Soporte Técnico
def soporte_tecnico_base_conocimiento(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Soporte Técnico",
        "section_title": "Base de conocimiento",
        "section_description": "Sección para consultar artículos, guías y soluciones a problemas frecuentes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def soporte_tecnico_tickets(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Soporte Técnico",
        "section_title": "Tickets de soporte",
        "section_description": "Gestión de tickets de soporte abiertos por usuarios del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def soporte_tecnico_contacto_proveedor(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Soporte Técnico",
        "section_title": "Contacto con proveedor",
        "section_description": "Información y herramientas para contactar al proveedor o al área de soporte externo."
    }
    return render(request, 'parking/dashboard_section.html', context)

def soporte_tecnico_guias_usuario(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Soporte Técnico",
        "section_title": "Guías de usuario",
        "section_description": "Listado de manuales y guías paso a paso para el uso del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 9.2 Mantenimiento del Sistema
def soporte_mantenimiento_backups(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Mantenimiento del Sistema",
        "section_title": "Copias de seguridad",
        "section_description": "Gestión y programación de copias de seguridad de la base de datos y archivos."
    }
    return render(request, 'parking/dashboard_section.html', context)

def soporte_mantenimiento_actualizaciones(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Mantenimiento del Sistema",
        "section_title": "Actualizaciones",
        "section_description": "Control de versiones y despliegue de actualizaciones del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def soporte_mantenimiento_logs(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Mantenimiento del Sistema",
        "section_title": "Logs del sistema",
        "section_description": "Consulta de registros de eventos y errores del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def soporte_mantenimiento_diagnostico(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Mantenimiento del Sistema",
        "section_title": "Diagnóstico de problemas",
        "section_description": "Herramientas para diagnosticar y analizar problemas técnicos del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 9.3 Capacitación
def soporte_capacitacion_manuales(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Capacitación",
        "section_title": "Manuales de uso",
        "section_description": "Repositorio de manuales de uso para diferentes perfiles del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def soporte_capacitacion_videos(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Capacitación",
        "section_title": "Videos tutoriales",
        "section_description": "Sección para alojar y consultar videos tutoriales de capacitación."
    }
    return render(request, 'parking/dashboard_section.html', context)

def soporte_capacitacion_sesiones(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Capacitación",
        "section_title": "Sesiones de entrenamiento",
        "section_description": "Gestión de sesiones de entrenamiento en vivo o programadas para usuarios."
    }
    return render(request, 'parking/dashboard_section.html', context)

def soporte_capacitacion_material(request):
    context = {
        "section_group": "Soporte y Mantenimiento - Capacitación",
        "section_title": "Material de referencia",
        "section_description": "Documentos, presentaciones y otros materiales de referencia para capacitación."
    }
    return render(request, 'parking/dashboard_section.html', context)

# ===============10. HERRAMIENTAS ADICIONALES=============
# 10.1 Comunicaciones
def herr_comunicaciones_notificaciones(request):
    context = {
        "section_group": "Herramientas Adicionales - Comunicaciones",
        "section_title": "Notificaciones a clientes",
        "section_description": "Configuración y envío de notificaciones a clientes (email, SMS, etc.)."
    }
    return render(request, 'parking/dashboard_section.html', context)

def herr_comunicaciones_recordatorios(request):
    context = {
        "section_group": "Herramientas Adicionales - Comunicaciones",
        "section_title": "Recordatorios de reservas",
        "section_description": "Gestión de recordatorios automáticos para reservas próximas."
    }
    return render(request, 'parking/dashboard_section.html', context)

def herr_comunicaciones_alertas_sistema(request):
    context = {
        "section_group": "Herramientas Adicionales - Comunicaciones",
        "section_title": "Alertas del sistema",
        "section_description": "Configuración de alertas internas sobre eventos importantes del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def herr_comunicaciones_mensajes_masivos(request):
    context = {
        "section_group": "Herramientas Adicionales - Comunicaciones",
        "section_title": "Mensajes masivos",
        "section_description": "Envío de campañas de mensajes masivos a grupos de clientes."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 10.2 Inventario
def herr_inventario_control_insumos(request):
    context = {
        "section_group": "Herramientas Adicionales - Inventario",
        "section_title": "Control de insumos",
        "section_description": "Gestión de insumos necesarios para la operación del parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def herr_inventario_productos_adicionales(request):
    context = {
        "section_group": "Herramientas Adicionales - Inventario",
        "section_title": "Productos adicionales (lavado, etc.)",
        "section_description": "Administración de productos y servicios adicionales como lavado, encerado, etc."
    }
    return render(request, 'parking/dashboard_section.html', context)

def herr_inventario_movimientos(request):
    context = {
        "section_group": "Herramientas Adicionales - Inventario",
        "section_title": "Movimientos de inventario",
        "section_description": "Registro de entradas y salidas de inventario asociado al parqueadero."
    }
    return render(request, 'parking/dashboard_section.html', context)

def herr_inventario_alertas_stock(request):
    context = {
        "section_group": "Herramientas Adicionales - Inventario",
        "section_title": "Alertas de stock",
        "section_description": "Configuración de alertas cuando el stock de insumos llegue a mínimos."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 10.3 Marketing
def herr_marketing_campanas(request):
    context = {
        "section_group": "Herramientas Adicionales - Marketing",
        "section_title": "Campañas promocionales",
        "section_description": "Gestión de campañas promocionales para atraer y fidelizar clientes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def herr_marketing_cupones(request):
    context = {
        "section_group": "Herramientas Adicionales - Marketing",
        "section_title": "Cupones de descuento",
        "section_description": "Creación y control de cupones de descuento aplicables en el POS."
    }
    return render(request, 'parking/dashboard_section.html', context)

def herr_marketing_referidos(request):
    context = {
        "section_group": "Herramientas Adicionales - Marketing",
        "section_title": "Programas de referidos",
        "section_description": "Configuración de programas de referidos entre clientes."
    }
    return render(request, 'parking/dashboard_section.html', context)

def herr_marketing_encuestas(request):
    context = {
        "section_group": "Herramientas Adicionales - Marketing",
        "section_title": "Encuestas de satisfacción",
        "section_description": "Gestión de encuestas para medir la satisfacción de los clientes."
    }
    return render(request, 'parking/dashboard_section.html', context)

# ===========11. SEGURIDAD Y AUDITORÍA===========
# 11.1 Control de Accesos
def seguridad_control_registro(request):
    context = {
        "section_group": "Seguridad y Auditoría - Control de Accesos",
        "section_title": "Registro de entradas/salidas",
        "section_description": "Listado y búsqueda de ingresos y salidas de usuarios en el sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def seguridad_control_usuarios_conectados(request):
    context = {
        "section_group": "Seguridad y Auditoría - Control de Accesos",
        "section_title": "Usuarios conectados",
        "section_description": "Visualización de los usuarios que actualmente están conectados al sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def seguridad_control_intentos_fallidos(request):
    context = {
        "section_group": "Seguridad y Auditoría - Control de Accesos",
        "section_title": "Intentos fallidos",
        "section_description": "Registro de intentos fallidos de acceso y posibles intentos de intrusión."
    }
    return render(request, 'parking/dashboard_section.html', context)

def seguridad_control_bloqueos(request):
    context = {
        "section_group": "Seguridad y Auditoría - Control de Accesos",
        "section_title": "Bloqueos de seguridad",
        "section_description": "Gestión de cuentas bloqueadas y reglas de bloqueo de seguridad."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 11.2 Auditoría
def seguridad_auditoria_log_transacciones(request):
    context = {
        "section_group": "Seguridad y Auditoría - Auditoría",
        "section_title": "Log de transacciones",
        "section_description": "Registro detallado de las transacciones realizadas en el sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def seguridad_auditoria_cambios_sistema(request):
    context = {
        "section_group": "Seguridad y Auditoría - Auditoría",
        "section_title": "Cambios en el sistema",
        "section_description": "Historial de cambios de configuración y actualizaciones realizadas."
    }
    return render(request, 'parking/dashboard_section.html', context)

def seguridad_auditoria_reportes(request):
    context = {
        "section_group": "Seguridad y Auditoría - Auditoría",
        "section_title": "Reportes de seguridad",
        "section_description": "Generación de reportes relacionados con la seguridad del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

def seguridad_auditoria_trazabilidad(request):
    context = {
        "section_group": "Seguridad y Auditoría - Auditoría",
        "section_title": "Trazabilidad de operaciones",
        "section_description": "Seguimiento de quién hizo qué y cuándo dentro del sistema."
    }
    return render(request, 'parking/dashboard_section.html', context)

# ===========12. SISTEMA DE ALERTAS==================
# 12.1 Alertas Operativas
def alertas_operativas_espacios_llenos(request):
    context = {
        "section_group": "Sistema de Alertas - Alertas Operativas",
        "section_title": "Espacios llenos",
        "section_description": "Alertas cuando la ocupación del parqueadero o de una zona alcanza el límite establecido."
    }
    return render(request, 'parking/dashboard_section.html', context)

def alertas_operativas_vehiculos_tiempo(request):
    context = {
        "section_group": "Sistema de Alertas - Alertas Operativas",
        "section_title": "Vehículos excediendo tiempo",
        "section_description": "Alertas sobre vehículos que superan el tiempo máximo permitido de permanencia."
    }
    return render(request, 'parking/dashboard_section.html', context)

def alertas_operativas_dispositivos(request):
    context = {
        "section_group": "Sistema de Alertas - Alertas Operativas",
        "section_title": "Problemas con dispositivos",
        "section_description": "Notificaciones sobre fallos o desconexiones de dispositivos (cámaras, barreras, impresoras, etc.)."
    }
    return render(request, 'parking/dashboard_section.html', context)

def alertas_operativas_incidentes(request):
    context = {
        "section_group": "Sistema de Alertas - Alertas Operativas",
        "section_title": "Incidentes de seguridad",
        "section_description": "Registro y alertas relacionadas con incidentes o eventos de seguridad."
    }
    return render(request, 'parking/dashboard_section.html', context)

# 12.2 Alertas Financieras
def alertas_financieras_cierres_pendientes(request):
    context = {
        "section_group": "Sistema de Alertas - Alertas Financieras",
        "section_title": "Cierres pendientes",
        "section_description": "Alertas cuando existan cierres de caja pendientes de realizar o confirmar."
    }
    return render(request, 'parking/dashboard_section.html', context)

def alertas_financieras_pagos_atrasados(request):
    context = {
        "section_group": "Sistema de Alertas - Alertas Financieras",
        "section_title": "Pagos atrasados",
        "section_description": "Notificaciones de pagos vencidos o cuotas atrasadas de clientes o convenios."
    }
    return render(request, 'parking/dashboard_section.html', context)

def alertas_financieras_objetivos_venta(request):
    context = {
        "section_group": "Sistema de Alertas - Alertas Financieras",
        "section_title": "Objetivos de venta",
        "section_description": "Alertas sobre cumplimiento o incumplimiento de metas de ingresos y ventas."
    }
    return render(request, 'parking/dashboard_section.html', context)

def alertas_financieras_anomalias_ingresos(request):
    context = {
        "section_group": "Sistema de Alertas - Alertas Financieras",
        "section_title": "Anomalías en ingresos",
        "section_description": "Detección de comportamientos atípicos en los ingresos (picos, caídas inesperadas, etc.)."
    }
    return render(request, 'parking/dashboard_section.html', context)
