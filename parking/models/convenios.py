from django.db import models
from .clientes import EmpresaCorporativa

class ConvenioEmpresa(models.Model):
    # CONEXIÓN MULTI-TENANT
    parqueadero = models.ForeignKey(
        'parking.Parqueadero',
        on_delete=models.CASCADE,
        related_name="convenios_empresa",
        null=True, blank=True
    )

    empresa = models.CharField("Nombre de la empresa", max_length=150)
    nit = models.CharField("NIT", max_length=30, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField("Correo electrónico", blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["empresa"]
        verbose_name = "Empresa en convenio"
        verbose_name_plural = "Empresas en convenio"

    def __str__(self):
        return f"{self.empresa} ({self.nit})"


class ConvenioEmpresaLimites(models.Model):
    empresa = models.ForeignKey(ConvenioEmpresa, on_delete=models.CASCADE, related_name="limites")
    max_vehiculos_simultaneos = models.PositiveIntegerField(blank=True, null=True, verbose_name="Cupo simultáneo máximo")
    max_ingresos_dia = models.PositiveIntegerField(blank=True, null=True, verbose_name="Máximos ingresos por día")
    max_ingresos_mes = models.PositiveIntegerField(blank=True, null=True, verbose_name="Máx. ingresos por mes")
    max_horas_por_ingreso = models.PositiveIntegerField(blank=True, null=True, verbose_name="Máx. horas por ingreso")
    permitir_carros = models.BooleanField(default=True)
    permitir_motos = models.BooleanField(default=True)
    permitir_bicicletas = models.BooleanField(default=True)
    aplica_fines_semana = models.BooleanField(default=True, verbose_name="Aplica fines de semana")
    aplica_festivos = models.BooleanField(default=True, verbose_name="Aplica festivos")

    class Meta:
        verbose_name = "Límites y restricciones de convenio"
        verbose_name_plural = "Límites y restricciones de convenios"

    def __str__(self):
        return f"Límites · {self.empresa}"


class TarifaEspecialConvenio(models.Model):
    TIPO_BENEFICIO_CHOICES = (
        ("MINUTOS_CORTESIA", "Minutos de cortesía"),
        ("DESCUENTO_PORCENTAJE", "Descuento %"),
        ("DESCUENTO_VALOR", "Descuento valor fijo"),
        ("TARIFA_FIJA", "Tarifa fija"),
    )

    APLICACION_CHOICES = (
        ("POR_VISITA", "Por visita"),
        ("POR_DIA", "Por día"),
    )

    empresa_convenio = models.ForeignKey(ConvenioEmpresa, on_delete=models.CASCADE, related_name="tarifas_especiales", verbose_name="Empresa en convenio")
    tipo_beneficio = models.CharField(max_length=30, choices=TIPO_BENEFICIO_CHOICES)
    valor_beneficio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Minutos, porcentaje o valor.")
    consumo_minimo = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Compra mínima.")
    aplicacion = models.CharField(max_length=20, choices=APLICACION_CHOICES, default="POR_VISITA")
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["empresa_convenio__empresa", "tipo_beneficio"]
        verbose_name = "Tarifa especial de convenio"
        verbose_name_plural = "Tarifas especiales de convenio"

    def __str__(self):
        return f"{self.empresa_convenio.empresa} - {self.tipo_beneficio}"


class ConvenioVigencia(models.Model):
    empresa_convenio = models.ForeignKey(ConvenioEmpresa, on_delete=models.CASCADE, related_name="vigencias", verbose_name="Empresa en convenio")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    descripcion = models.CharField(max_length=200, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["empresa_convenio__empresa", "fecha_inicio"]
        verbose_name = "Período de vigencia"
        verbose_name_plural = "Períodos de vigencia"

    def __str__(self):
        return f"{self.empresa_convenio.empresa} [{self.fecha_inicio} - {self.fecha_fin}]"


class RestriccionHorariaConvenio(models.Model):
    DIA_SEMANA_CHOICES = (
        ("LUNES", "Lunes"),
        ("MARTES", "Martes"),
        ("MIERCOLES", "Miércoles"),
        ("JUEVES", "Jueves"),
        ("VIERNES", "Viernes"),
        ("SABADO", "Sábado"),
        ("DOMINGO", "Domingo"),
    )

    empresa_convenio = models.ForeignKey(ConvenioEmpresa, on_delete=models.CASCADE, related_name="restricciones_horarias", verbose_name="Empresa en convenio")
    dia_semana = models.CharField(max_length=10, choices=DIA_SEMANA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["empresa_convenio__empresa", "dia_semana", "hora_inicio"]
        verbose_name = "Restricción horaria de convenio"
        verbose_name_plural = "Restricciones horarias de convenio"

    def __str__(self):
        return f"{self.empresa_convenio.empresa} - {self.dia_semana} {self.hora_inicio}-{self.hora_fin}"


class TerminoPagoEmpresa(models.Model):
    TIPO_CHOICES = (
        ("CONTADO", "Contado"),
        ("CREDITO", "Crédito"),
    )

    ESTADO_CHOICES = (
        ("ACTIVO", "Activo"),
        ("SUSPENDIDO", "Suspendido"),
    )

    empresa = models.OneToOneField(EmpresaCorporativa, on_delete=models.CASCADE, related_name="terminos_pago")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default="CONTADO")
    dias_credito = models.PositiveIntegerField(default=0)
    cupo_credito = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    dia_corte = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Día del mes del corte (1–31)")
    dia_pago = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Día del mes de pago (1–31)")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="ACTIVO")
    notas = models.TextField(blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Término de pago"
        verbose_name_plural = "Términos de pago"

    def __str__(self):
        return f"{self.empresa.razon_social} - {self.get_tipo_display()}"