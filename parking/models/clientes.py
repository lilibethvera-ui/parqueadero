from django.db import models

TIPO_VEHICULO_CHOICES = (
    ("CARRO", "Carro"),
    ("MOTO", "Moto"),
    ("CAMIONETA", "Camioneta"),
    ("OTRO", "Otro"),
)

class Cliente(models.Model):
    TIPO_CLIENTE_CHOICES = (
        ("FRECUENTE", "Cliente frecuente"),
        ("CORPORATIVO", "Cliente corporativo"),
    )

    # CONEXIÓN MULTI-TENANT: Cada cliente pertenece a un parqueadero específico
    parqueadero = models.ForeignKey(
        'parking.Parqueadero',
        on_delete=models.CASCADE,
        related_name="clientes",
        null=True, blank=True # Permisivo temporal por si tienes datos de prueba previos
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CLIENTE_CHOICES,
        default="FRECUENTE",
        help_text="Define si es un cliente frecuente o corporativo."
    )

    # Datos básicos
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150, blank=True)
    documento = models.CharField(
        max_length=50,
        unique=True,
        help_text="Documento de identidad, NIT u otro identificador."
    )

    # Contacto
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)

    nombre_empresa = models.CharField(
        max_length=200,
        blank=True,
        help_text="Solo para clientes corporativos."
    )

    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre", "apellidos"]
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        if self.nombre_empresa:
            return f"{self.nombre_empresa} ({self.documento})"
        return f"{self.nombre} {self.apellidos} ({self.documento})".strip()


class Vehiculo(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="vehiculos"
    )
    placa = models.CharField(
        max_length=10,
        help_text="Placa del vehículo."
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_VEHICULO_CHOICES,
        default="CARRO"
    )

    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["placa"]
        unique_together = ("cliente", "placa")
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f"{self.placa} - {self.cliente}"


class EmpresaCorporativa(models.Model):
    ESTADO_CHOICES = (
        ("ACTIVA", "Activa"),
        ("INACTIVA", "Inactiva"),
    )

    # CONEXIÓN MULTI-TENANT
    parqueadero = models.ForeignKey(
        'parking.Parqueadero',
        on_delete=models.CASCADE,
        related_name="empresas_corporativas",
        null=True, blank=True
    )

    contacto = models.ForeignKey(
        "ContactoAutorizado",
        on_delete=models.PROTECT,
        related_name="empresas_corporativas",
        help_text="Contacto authorized principal para la empresa.",
        null=True,
        blank=True,
    )

    nit = models.CharField("NIT", max_length=30, unique=True)
    razon_social = models.CharField("Razón social", max_length=150)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="ACTIVA")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["razon_social"]

    def __str__(self):
        return f"{self.razon_social} ({self.nit})"


class ContactoAutorizado(models.Model):
    empresa = models.ForeignKey(
        "EmpresaCorporativa",
        on_delete=models.CASCADE,
        related_name="contactos_autorizados",
    )
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["empresa__razon_social", "nombre"]

    def __str__(self):
        return f"{self.nombre} - {self.empresa.razon_social}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.activo and self.empresa and self.empresa.contacto_id is None:
            self.empresa.contacto = self
            self.empresa.save(update_fields=["contacto"])


class VehiculoAutorizado(models.Model):
    empresa = models.ForeignKey(
        EmpresaCorporativa,
        on_delete=models.CASCADE,
        related_name="vehiculos_autorizados",
    )
    placa = models.CharField(max_length=15)
    tipo_vehiculo = models.CharField(max_length=50, blank=True)
    descripcion = models.CharField(
        max_length=150,
        blank=True,
        help_text="Ej: Camioneta blanca, carro del gerente, etc."
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["empresa__razon_social", "placa"]
        verbose_name = "Vehículo autorizado"
        verbose_name_plural = "Vehículos autorizados"

    def __str__(self):
        return f"{self.placa} - {self.empresa.razon_social}"


class Estacionamiento(models.Model):
    ESTADO_CHOICES = (
        ("EN_CURSO", "En curso"),
        ("FINALIZADO", "Finalizado"),
        ("ANULADO", "Anulado"),
    )

    METODO_PAGO_CHOICES = (
        ("EFECTIVO", "Efectivo"),
        ("TARJETA", "Tarjeta"),
        ("TRANSFERENCIA", "Transferencia"),
        ("OTRO", "Otro"),
    )

    # CONEXIÓN MULTI-TENANT (Directa para acelerar el filtrado de transacciones en vivo)
    parqueadero = models.ForeignKey(
        'parking.Parqueadero',
        on_delete=models.CASCADE,
        related_name="estacionamientos",
        null=True, blank=True
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="estacionamientos")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True, related_name="estacionamientos")
    
    fecha_hora_entrada = models.DateTimeField()
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)
    tarifa_aplicada = models.CharField(max_length=150, blank=True, help_text="Nombre de la tarifa usada.")
    valor_cobrado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default="EFECTIVO")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="EN_CURSO")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_hora_entrada"]
        verbose_name = "Estacionamiento"
        verbose_name_plural = "Estacionamientos"

    def __str__(self):
        return f"{self.cliente} · {self.vehiculo} · {self.fecha_hora_entrada}"

    @property
    def duracion_minutos(self):
        if not self.fecha_hora_salida:
            return None
        delta = self.fecha_hora_salida - self.fecha_hora_entrada
        return int(delta.total_seconds() // 60)

    @property
    def duracion_legible(self):
        mins = self.duracion_minutos
        if mins is None:
            return "En curso"
        horas = mins // 60
        resto = mins % 60
        if horas and resto:
            return f"{horas} h {resto} min"
        elif horas:
            return f"{horas} h"
        return f"{resto} min"