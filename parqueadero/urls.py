from django.contrib import admin
from django.urls import path, include
from parking import views as parking_views
from django.contrib.auth import views as auth_views
from parking.views import tarifas_views 
from parking.views import clientes_views
from parking.views import convenios_views
from parking.views import usuarios_views


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', parking_views.dashboard_resumen_general, name='dashboard'),

    path('login/', usuarios_views.login_view, name='login'),
    path('registro/', parking_views.registro_view, name='registro'),
    path('logout/', usuarios_views.logout_view, name='logout'),
    path('seleccionar-sucursal/', usuarios_views.seleccionar_sucursal_view, name='seleccionar_sucursal'),
    path('validar-username/', usuarios_views.validar_username, name='validar_username'),
    path('validar-email/', usuarios_views.validar_email, name='validar_email'),

    # ======= RESUMEN GENERAL ================
    path('dashboard/estado-actual/', parking_views.dashboard_estado_actual, name='dashboard_estado_actual'),
    path('dashboard/resumen-general/', parking_views.dashboard_resumen_general, name='dashboard_resumen_general'),
    path('dashboard/ocupacion-tiempo-real/', parking_views.dashboard_ocupacion_tiempo_real, name='dashboard_ocupacion_tiempo_real'),
    path('dashboard/ingresos-dia/', parking_views.dashboard_ingresos_dia, name='dashboard_ingresos_dia'),
    path('dashboard/vehiculos-actuales/', parking_views.dashboard_vehiculos_actuales, name='dashboard_vehiculos_actuales'),
    
    
    # MÉTRICAS CLAVE
    path('dashboard/ingresos-periodos/', parking_views.dashboard_ingresos_periodos, name='dashboard_ingresos_periodos'),
    path('dashboard/tasa-ocupacion-promedio/', parking_views.dashboard_tasa_ocupacion_promedio, name='dashboard_tasa_ocupacion_promedio'),
    path('dashboard/vehiculos-frecuentes/', parking_views.dashboard_vehiculos_frecuentes, name='dashboard_vehiculos_frecuentes'),
    path('dashboard/horarios-pico/', parking_views.dashboard_horarios_pico, name='dashboard_horarios_pico'),

    # ========== POS - PUNTO DE VENTA =======
    # 2.1 Registro de Ingresos
    path('pos/ingresos/entrada/', parking_views.pos_ingresos_entrada, name='pos_ingresos_entrada'),
    path('pos/ingresos/tipo-vehiculo/', parking_views.pos_ingresos_tipo_vehiculo, name='pos_ingresos_tipo_vehiculo'),
    path('pos/ingresos/asignar-espacio/', parking_views.pos_ingresos_asignar_espacio, name='pos_ingresos_asignar_espacio'),
    path('pos/ingresos/fotografia/', parking_views.pos_ingresos_fotografia, name='pos_ingresos_fotografia'),
    path('pos/ingresos/ticket/', parking_views.pos_ingresos_ticket, name='pos_ingresos_ticket'),

    # 2.2 Registro de Salidas
    path('pos/salidas/tiempo/', parking_views.pos_salidas_tiempo, name='pos_salidas_tiempo'),
    path('pos/salidas/tarifas/', parking_views.pos_salidas_tarifas, name='pos_salidas_tarifas'),
    path('pos/salidas/pago/efectivo/', parking_views.pos_salidas_pago_efectivo, name='pos_salidas_pago_efectivo'),
    path('pos/salidas/pago/tarjeta/', parking_views.pos_salidas_pago_tarjeta, name='pos_salidas_pago_tarjeta'),
    path('pos/salidas/pago/transferencia/', parking_views.pos_salidas_pago_transferencia, name='pos_salidas_pago_transferencia'),
    path('pos/salidas/pago/convenios/', parking_views.pos_salidas_pago_convenios, name='pos_salidas_pago_convenios'),
    path('pos/salidas/factura/', parking_views.pos_salidas_factura, name='pos_salidas_factura'),

    # 2.3 Reservas
    path('pos/reservas/crear/', parking_views.pos_reservas_crear, name='pos_reservas_crear'),
    path('pos/reservas/modificar/', parking_views.pos_reservas_modificar, name='pos_reservas_modificar'),
    path('pos/reservas/cancelar/', parking_views.pos_reservas_cancelar, name='pos_reservas_cancelar'),
    path('pos/reservas/calendario/', parking_views.pos_reservas_calendario, name='pos_reservas_calendario'),

    # ================== GESTIÓN DE TARIFAS =====================
    # Tarifas base
    path("tarifas/base-tiempo/", tarifas_views.tarifa_base_tiempo_list_create, name="tarifas_base_tiempo"),
    path("tarifas/base-tiempo/<int:pk>/toggle/", tarifas_views.tarifa_base_tiempo_toggle_activo, name="tarifa_base_tiempo_toggle"),
    path("tarifas/base-tiempo/<int:pk>/inline-update/", tarifas_views.tarifa_base_tiempo_inline_update, name="tarifa_base_tiempo_inline_update"),
    path("tarifas/base-diaria/", tarifas_views.tarifa_base_diaria_list_create, name="tarifas_base_diaria"),
    path("tarifas/base-diaria/<int:pk>/inline/", tarifas_views.tarifa_base_diaria_inline_update, name="tarifa_base_diaria_inline_update"),
    path("tarifas/base-diaria/<int:pk>/toggle/", tarifas_views.tarifa_base_diaria_toggle, name="tarifa_base_diaria_toggle"),
    path("tarifas/base-dia-noche/", tarifas_views.tarifas_base_dia_noche, name="tarifas_base_dia_noche"),
    path('tarifas/update/<str:model_type>/<int:pk>/', tarifas_views.tarifa_inline_update, name='tarifa_inline_update'),
    path("tarifas/base-diaria/<int:pk>/inline/", tarifas_views.tarifa_base_diaria_inline_update, name="tarifa_base_diaria_inline_update"),
    path("tarifas/base-diaria/<int:pk>/toggle/", tarifas_views.tarifa_base_diaria_toggle, name="tarifa_base_diaria_toggle"),
    path("tarifas/base-nocturna/<int:pk>/inline/", tarifas_views.tarifa_base_nocturna_inline_update, name="tarifa_base_nocturna_inline_update"),
    path("tarifas/base-nocturna/<int:pk>/toggle/", tarifas_views.tarifa_base_nocturna_toggle, name="tarifa_base_nocturna_toggle"),

    path('tarifas/base/fines-semana/', parking_views.tarifas_base_fines_semana, name='tarifas_base_fines_semana'),

    # Tarifas especiales
    path('tarifas/especiales/tipo-vehiculo/', parking_views.tarifas_especiales_tipo_vehiculo, name='tarifas_especiales_tipo_vehiculo'),
    path('tarifas/especiales/promocionales/', parking_views.tarifas_especiales_promocionales, name='tarifas_especiales_promocionales'),
    path('tarifas/especiales/descuentos-volumen/', parking_views.tarifas_especiales_descuentos_volumen, name='tarifas_especiales_descuentos_volumen'),
    path('tarifas/especiales/temporada/', parking_views.tarifas_especiales_temporada, name='tarifas_especiales_temporada'),

    # Paquetes y planes
    path('tarifas/paquetes/mensualidad/', parking_views.tarifas_paquetes_mensualidad, name='tarifas_paquetes_mensualidad'),
    path('tarifas/paquetes/corporativos/', parking_views.tarifas_paquetes_corporativos, name='tarifas_paquetes_corporativos'),
    path('tarifas/paquetes/promocionales/', parking_views.tarifas_paquetes_promocionales, name='tarifas_paquetes_promocionales'),
     
    # ====== 4. GESTIÓN DE CONVENIOS =========
    # Empresas Convenio
    path('convenios/empresas/registrar/', convenios_views.convenios_empresas_registrar, name='convenios_empresas_registrar'),
    path('convenios/empresas/limites/', convenios_views.convenios_control_limites_restricciones, name='convenios_empresas_limites'),

    # Tarifas de Convenio
    path('convenios/tarifas/configurar/', convenios_views.convenios_tarifas_configurar, name='convenios_tarifas_configurar'),
    path('convenios/tarifas/vigencia/', convenios_views.convenios_tarifas_vigencia, name='convenios_tarifas_vigencia'),

    # Control de Acceso
    path('convenios/control/restricciones-horarias/', convenios_views.convenios_control_restricciones_horarias, name='convenios_control_restricciones_horarias'),
    
    # ========= 5. GESTIÓN DE CLIENTES==========
    # Clientes Frecuentes
    path("clientes/frecuentes/",clientes_views.clientes_frecuentes_listado,name="clientes_frecuentes_listado",),
    path("clientes/frecuentes/historial/",clientes_views.clientes_frecuentes_historial,name="clientes_frecuentes_historial",),

    # Clientes Corporativos
    path("clientes/corporativos/info-empresa/",clientes_views.clientes_corporativos_info_empresa,name="clientes_corporativos_info_empresa"),
    path("clientes/corporativos/contactos-autorizados/",clientes_views.clientes_corporativos_contactos_autorizados,name="clientes_corporativos_contactos_autorizados"),
    path("clientes/corporativos/vehiculos-registrados/",clientes_views.clientes_corporativos_vehiculos_registrados,name="clientes_corporativos_vehiculos_registrados",),
    path('clientes/corporativos/terminos-pago/', clientes_views.clientes_corporativos_terminos_pago, name='clientes_corporativos_terminos_pago'),

    # 5.3 Programas de Fidelidad
    path('clientes/fidelidad/puntos/', parking_views.clientes_fidelidad_puntos, name='clientes_fidelidad_puntos'),
    path('clientes/fidelidad/beneficios/', parking_views.clientes_fidelidad_beneficios, name='clientes_fidelidad_beneficios'),
    path('clientes/fidelidad/niveles/', parking_views.clientes_fidelidad_niveles, name='clientes_fidelidad_niveles'),

        # =======================================
    # 6. REPORTES Y ANÁLISIS
    # =======================================

    # 6.1 Reportes Financieros
    path('reportes/financieros/ingresos/', parking_views.reportes_financieros_ingresos, name='reportes_financieros_ingresos'),
    path('reportes/financieros/flujo-caja/', parking_views.reportes_financieros_flujo_caja, name='reportes_financieros_flujo_caja'),
    path('reportes/financieros/comparativos/', parking_views.reportes_financieros_comparativos, name='reportes_financieros_comparativos'),
    path('reportes/financieros/tendencias/', parking_views.reportes_financieros_tendencias, name='reportes_financieros_tendencias'),

    # 6.2 Reportes Operativos
    path('reportes/operativos/ocupacion-horarios/', parking_views.reportes_operativos_ocupacion_horarios, name='reportes_operativos_ocupacion_horarios'),
    path('reportes/operativos/tipos-vehiculos/', parking_views.reportes_operativos_tipos_vehiculos, name='reportes_operativos_tipos_vehiculos'),
    path('reportes/operativos/tiempos-permanencia/', parking_views.reportes_operativos_tiempos_permanencia, name='reportes_operativos_tiempos_permanencia'),
    path('reportes/operativos/espacios-mas-utilizados/', parking_views.reportes_operativos_espacios_mas_utilizados, name='reportes_operativos_espacios_mas_utilizados'),

    # 6.3 Reportes de Clientes
    path('reportes/clientes/frecuentes/', parking_views.reportes_clientes_frecuentes, name='reportes_clientes_frecuentes'),
    path('reportes/clientes/comportamiento-uso/', parking_views.reportes_clientes_comportamiento_uso, name='reportes_clientes_comportamiento_uso'),
    path('reportes/clientes/preferencias-pago/', parking_views.reportes_clientes_preferencias_pago, name='reportes_clientes_preferencias_pago'),

    # 6.4 Reportes Personalizados
    path('reportes/personalizados/filtros/', parking_views.reportes_personalizados_filtros, name='reportes_personalizados_filtros'),
    path('reportes/personalizados/exportacion/', parking_views.reportes_personalizados_exportacion, name='reportes_personalizados_exportacion'),
    path('reportes/personalizados/graficos/', parking_views.reportes_personalizados_graficos, name='reportes_personalizados_graficos'),

        # =======================================
    # 7. CONFIGURACIÓN DEL SISTEMA
    # =======================================

    # 7.1 Configuración General
    path('configuracion/general/datos-negocio/', parking_views.config_sistema_general_datos_negocio, name='config_sistema_general_datos_negocio'),
    path('configuracion/general/horarios/', parking_views.config_sistema_general_horarios, name='config_sistema_general_horarios'),
    path('configuracion/general/impuestos/', parking_views.config_sistema_general_impuestos, name='config_sistema_general_impuestos'),
    path('configuracion/general/moneda-formatos/', parking_views.config_sistema_general_moneda_formatos, name='config_sistema_general_moneda_formatos'),

    # 7.2 Configuración de Espacios
    path('configuracion/espacios/mapa/', parking_views.config_espacios_mapa, name='config_espacios_mapa'),
    path('configuracion/espacios/tipos/', parking_views.config_espacios_tipos, name='config_espacios_tipos'),
    path('configuracion/espacios/zonas/', parking_views.config_espacios_zonas, name='config_espacios_zonas'),
    path('configuracion/espacios/especiales/', parking_views.config_espacios_especiales, name='config_espacios_especiales'),

    # 7.3 Configuración de Dispositivos
    path('configuracion/dispositivos/impresoras/', parking_views.config_dispositivos_impresoras, name='config_dispositivos_impresoras'),
    path('configuracion/dispositivos/lectores/', parking_views.config_dispositivos_lectores, name='config_dispositivos_lectores'),
    path('configuracion/dispositivos/camaras/', parking_views.config_dispositivos_camaras, name='config_dispositivos_camaras'),
    path('configuracion/dispositivos/barreras/', parking_views.config_dispositivos_barreras, name='config_dispositivos_barreras'),

    # 7.4 Usuarios y Permisos
    path('configuracion/usuarios/crear/', parking_views.config_usuarios_crear, name='config_usuarios_crear'),
    path('configuracion/usuarios/roles-permisos/', parking_views.config_usuarios_roles_permisos, name='config_usuarios_roles_permisos'),
    path('configuracion/usuarios/horarios-acceso/', parking_views.config_usuarios_horarios_acceso, name='config_usuarios_horarios_acceso'),
    path('configuracion/usuarios/auditoria/', parking_views.config_usuarios_auditoria, name='config_usuarios_auditoria'),

        # =======================================
    # 8. MÓDULO CONTABLE
    # =======================================

    # 8.1 Cierre de Caja
    path('contable/cierre/arqueo/', parking_views.contable_cierre_arqueo, name='contable_cierre_arqueo'),
    path('contable/cierre/conciliacion/', parking_views.contable_cierre_conciliacion, name='contable_cierre_conciliacion'),
    path('contable/cierre/reporte-cierres/', parking_views.contable_cierre_reporte_cierres, name='contable_cierre_reporte_cierres'),
    path('contable/cierre/historico/', parking_views.contable_cierre_historico, name='contable_cierre_historico'),

    # 8.2 Facturación
    path('contable/facturacion/emision/', parking_views.contable_facturacion_emision, name='contable_facturacion_emision'),
    path('contable/facturacion/notas-credito/', parking_views.contable_facturacion_notas_credito, name='contable_facturacion_notas_credito'),
    path('contable/facturacion/control-series/', parking_views.contable_facturacion_control_series, name='contable_facturacion_control_series'),
    path('contable/facturacion/envio-electronico/', parking_views.contable_facturacion_envio_electronico, name='contable_facturacion_envio_electronico'),

    # 8.3 Cuentas por Cobrar
    path('contable/cxc/estado-cuentas/', parking_views.contable_cxc_estado_cuentas, name='contable_cxc_estado_cuentas'),
    path('contable/cxc/cartera-vencida/', parking_views.contable_cxc_cartera_vencida, name='contable_cxc_cartera_vencida'),
    path('contable/cxc/recordatorios-pago/', parking_views.contable_cxc_recordatorios_pago, name='contable_cxc_recordatorios_pago'),
    path('contable/cxc/conciliaciones/', parking_views.contable_cxc_conciliaciones, name='contable_cxc_conciliaciones'),

    # 8.4 Integraciones Contables
    path('contable/integraciones/exportacion/', parking_views.contable_integraciones_exportacion, name='contable_integraciones_exportacion'),
    path('contable/integraciones/formatos/', parking_views.contable_integraciones_formatos, name='contable_integraciones_formatos'),
    path('contable/integraciones/automatizacion/', parking_views.contable_integraciones_automatizacion, name='contable_integraciones_automatizacion'),

        # =======================================
    # 9. SOPORTE Y MANTENIMIENTO
    # =======================================

    # 9.1 Soporte Técnico
    path('soporte/tecnico/base-conocimiento/', parking_views.soporte_tecnico_base_conocimiento, name='soporte_tecnico_base_conocimiento'),
    path('soporte/tecnico/tickets/', parking_views.soporte_tecnico_tickets, name='soporte_tecnico_tickets'),
    path('soporte/tecnico/contacto-proveedor/', parking_views.soporte_tecnico_contacto_proveedor, name='soporte_tecnico_contacto_proveedor'),
    path('soporte/tecnico/guias-usuario/', parking_views.soporte_tecnico_guias_usuario, name='soporte_tecnico_guias_usuario'),

    # 9.2 Mantenimiento del Sistema
    path('soporte/mantenimiento/backups/', parking_views.soporte_mantenimiento_backups, name='soporte_mantenimiento_backups'),
    path('soporte/mantenimiento/actualizaciones/', parking_views.soporte_mantenimiento_actualizaciones, name='soporte_mantenimiento_actualizaciones'),
    path('soporte/mantenimiento/logs/', parking_views.soporte_mantenimiento_logs, name='soporte_mantenimiento_logs'),
    path('soporte/mantenimiento/diagnostico/', parking_views.soporte_mantenimiento_diagnostico, name='soporte_mantenimiento_diagnostico'),

    # 9.3 Capacitación
    path('soporte/capacitacion/manuales/', parking_views.soporte_capacitacion_manuales, name='soporte_capacitacion_manuales'),
    path('soporte/capacitacion/videos/', parking_views.soporte_capacitacion_videos, name='soporte_capacitacion_videos'),
    path('soporte/capacitacion/sesiones/', parking_views.soporte_capacitacion_sesiones, name='soporte_capacitacion_sesiones'),
    path('soporte/capacitacion/material/', parking_views.soporte_capacitacion_material, name='soporte_capacitacion_material'),

        # =======================================
    # 10. HERRAMIENTAS ADICIONALES
    # =======================================

    # 10.1 Comunicaciones
    path('herramientas/comunicaciones/notificaciones/', parking_views.herr_comunicaciones_notificaciones, name='herr_comunicaciones_notificaciones'),
    path('herramientas/comunicaciones/recordatorios/', parking_views.herr_comunicaciones_recordatorios, name='herr_comunicaciones_recordatorios'),
    path('herramientas/comunicaciones/alertas-sistema/', parking_views.herr_comunicaciones_alertas_sistema, name='herr_comunicaciones_alertas_sistema'),
    path('herramientas/comunicaciones/mensajes-masivos/', parking_views.herr_comunicaciones_mensajes_masivos, name='herr_comunicaciones_mensajes_masivos'),

    # 10.2 Inventario
    path('herramientas/inventario/control-insumos/', parking_views.herr_inventario_control_insumos, name='herr_inventario_control_insumos'),
    path('herramientas/inventario/productos-adicionales/', parking_views.herr_inventario_productos_adicionales, name='herr_inventario_productos_adicionales'),
    path('herramientas/inventario/movimientos/', parking_views.herr_inventario_movimientos, name='herr_inventario_movimientos'),
    path('herramientas/inventario/alertas-stock/', parking_views.herr_inventario_alertas_stock, name='herr_inventario_alertas_stock'),

    # 10.3 Marketing
    path('herramientas/marketing/campanas/', parking_views.herr_marketing_campanas, name='herr_marketing_campanas'),
    path('herramientas/marketing/cupones/', parking_views.herr_marketing_cupones, name='herr_marketing_cupones'),
    path('herramientas/marketing/referidos/', parking_views.herr_marketing_referidos, name='herr_marketing_referidos'),
    path('herramientas/marketing/encuestas/', parking_views.herr_marketing_encuestas, name='herr_marketing_encuestas'),

        # =======================================
    # 11. SEGURIDAD Y AUDITORÍA
    # =======================================

    # 11.1 Control de Accesos
    path('seguridad/control/registro/', parking_views.seguridad_control_registro, name='seguridad_control_registro'),
    path('seguridad/control/usuarios-conectados/', parking_views.seguridad_control_usuarios_conectados, name='seguridad_control_usuarios_conectados'),
    path('seguridad/control/intentos-fallidos/', parking_views.seguridad_control_intentos_fallidos, name='seguridad_control_intentos_fallidos'),
    path('seguridad/control/bloqueos/', parking_views.seguridad_control_bloqueos, name='seguridad_control_bloqueos'),

    # 11.2 Auditoría
    path('seguridad/auditoria/log-transacciones/', parking_views.seguridad_auditoria_log_transacciones, name='seguridad_auditoria_log_transacciones'),
    path('seguridad/auditoria/cambios-sistema/', parking_views.seguridad_auditoria_cambios_sistema, name='seguridad_auditoria_cambios_sistema'),
    path('seguridad/auditoria/reportes/', parking_views.seguridad_auditoria_reportes, name='seguridad_auditoria_reportes'),
    path('seguridad/auditoria/trazabilidad/', parking_views.seguridad_auditoria_trazabilidad, name='seguridad_auditoria_trazabilidad'),

        # =======================================
    # 12. SISTEMA DE ALERTAS
    # =======================================

    # 12.1 Alertas Operativas
    path('alertas/operativas/espacios-llenos/', parking_views.alertas_operativas_espacios_llenos, name='alertas_operativas_espacios_llenos'),
    path('alertas/operativas/vehiculos-tiempo/', parking_views.alertas_operativas_vehiculos_tiempo, name='alertas_operativas_vehiculos_tiempo'),
    path('alertas/operativas/dispositivos/', parking_views.alertas_operativas_dispositivos, name='alertas_operativas_dispositivos'),
    path('alertas/operativas/incidentes/', parking_views.alertas_operativas_incidentes, name='alertas_operativas_incidentes'),

    # 12.2 Alertas Financieras
    path('alertas/financieras/cierres-pendientes/', parking_views.alertas_financieras_cierres_pendientes, name='alertas_financieras_cierres_pendientes'),
    path('alertas/financieras/pagos-atrasados/', parking_views.alertas_financieras_pagos_atrasados, name='alertas_financieras_pagos_atrasados'),
    path('alertas/financieras/objetivos-venta/', parking_views.alertas_financieras_objetivos_venta, name='alertas_financieras_objetivos_venta'),
    path('alertas/financieras/anomalias-ingresos/', parking_views.alertas_financieras_anomalias_ingresos, name='alertas_financieras_anomalias_ingresos'),



    path('password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='parking/usuarios/password_reset.html',
        email_template_name='parking/usuarios/password_reset_email.html',
        subject_template_name='parking/usuarios/password_reset_subject.txt',
        success_url='/password-reset/done/'
    ),
    name='password_reset'),

    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='parking/usuarios/password_reset_done.html'
        ),
        name='password_reset_done'),
    
    path('password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='parking/usuarios/password_reset_confirm.html',
            success_url='/password-reset/complete/'
        ),
        name='password_reset_confirm'),
    
    path('password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='parking/usuarios/password_reset_complete.html'
        ),
        name='password_reset_complete'),


]
