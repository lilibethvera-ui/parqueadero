from django.db import models
from django.core.validators import MinValueValidator

TIPO_VEHICULO_CHOICES = (
    ("CARRO", "Carro"),
    ("MOTO", "Moto"),
    ("CAMIONETA", "Camioneta"),
    ("OTRO", "Otro"),
)

class TarifaBaseTiempo(models.Model):
    class Modo(models.TextChoices):
        HORA = "HORA", "Hora"
        FRACCION = "FRACCION", "Fracción"

    class Redondeo(models.TextChoices):
        ARRIBA = "ARRIBA", "Hacia arriba"
        EXACTO = "EXACTO", "Exacto"

    # CONEXIÓN MULTI-TENANT
    parqueadero = models.ForeignKey(
        'parking.Parqueadero',
        on_delete=models.CASCADE,
        related_name="tarifas_tiempo",
        null=True, blank=True
    )

    nombre = models.CharField(max_length=120, default="Base estándar")
    modo = models.CharField(max_length=20, choices=Modo.choices, default=Modo.FRACCION)
    minimo_minutos = models.PositiveIntegerField(default=0)
    redondeo = models.CharField(max_length=20, choices=Redondeo.choices, default=Redondeo.ARRIBA)
    precio_hora = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    tamano_fraccion_min = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    precio_fraccion = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_VEHICULO_CHOICES, default="CARRO")

    class Meta:
        db_table = "tarifa_base_tiempo"
        ordering = ["id"]

    def __str__(self):
        return f"{self.nombre} ({self.modo})"


class TarifaBaseDiaria(models.Model):
    MODO_DIARIA_CHOICES = (
        ("CALENDARIO", "Día calendario"),
        ("24H", "Cada 24 horas"),
    )

    # CONEXIÓN MULTI-TENANT
    parqueadero = models.ForeignKey(
        'parking.Parqueadero',
        on_delete=models.CASCADE,
        related_name="tarifas_diarias",
        null=True, blank=True
    )

    nombre = models.CharField(max_length=120)
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_VEHICULO_CHOICES, default="CARRO")
    modo_diaria = models.CharField(max_length=12, choices=MODO_DIARIA_CHOICES, default="CALENDARIO")
    hora_corte = models.TimeField(null=True, blank=True, help_text="Ej: 00:00 o 23:59")
    precio_dia = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["tipo_vehiculo", "nombre"]
        verbose_name = "Tarifa base diaria"
        verbose_name_plural = "Tarifas base diarias"

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_vehiculo_display()})"


class TarifaBaseNocturna(models.Model):
    class Modo(models.TextChoices):
        HORA = "HORA", "Hora"
        FRACCION = "FRACCION", "Fracción"

    class Redondeo(models.TextChoices):
        ARRIBA = "ARRIBA", "Arriba"
        EXACTO = "EXACTO", "Exacto"

    # CONEXIÓN MULTI-TENANT
    parqueadero = models.ForeignKey(
        'parking.Parqueadero',
        on_delete=models.CASCADE,
        related_name="tarifas_nocturnas",
        null=True, blank=True
    )

    nombre = models.CharField(max_length=120)
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_VEHICULO_CHOICES, default="CARRO")
    hora_inicio = models.TimeField(help_text="Ej: 18:00")
    hora_fin = models.TimeField(help_text="Ej: 06:00")
    modo = models.CharField(max_length=10, choices=Modo.choices, default=Modo.HORA)
    minimo_minutos = models.PositiveIntegerField(default=0)
    redondeo = models.CharField(max_length=10, choices=Redondeo.choices, default=Redondeo.ARRIBA)
    precio_hora = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tamano_fraccion_min = models.PositiveIntegerField(null=True, blank=True)
    precio_fraccion = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    activo = models.BooleanField(default=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["tipo_vehiculo", "nombre"]
        verbose_name = "Tarifa base nocturna"
        verbose_name_plural = "Tarifas base nocturnas"

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_vehiculo_display()})"