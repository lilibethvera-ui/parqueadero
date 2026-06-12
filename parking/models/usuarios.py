from django.db import models
from django.contrib.auth.models import AbstractUser

class EmpresaSaaS(models.Model):
    """El inquilino principal (Tenant). El dueño que te contrata el software (ej: Pepito Pérez S.A.)"""
    nombre_comercial = models.CharField(max_length=100, unique=True)
    nit = models.CharField(max_length=30, unique=True, blank=True, default='')
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_comercial


class Parqueadero(models.Model):
    """Las Sucursales físicas de la empresa (Branches)."""
    empresa = models.ForeignKey(EmpresaSaaS, on_delete=models.CASCADE, related_name='sucursales')
    nombre_sucursal = models.CharField(max_length=100)  # Ej: "Sede Norte", "Sede Centro"
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('empresa', 'nombre_sucursal') # Evita sucursales repetidas con el mismo nombre en la misma empresa

    def __str__(self):
        return f"{self.empresa.nombre_comercial} - {self.nombre_sucursal}"


class Usuario(AbstractUser):
    """Usuarios del sistema. Pertenecen a la empresa y pueden rotar entre sus sucursales."""
    ADMINISTRADOR = 'ADMIN'
    SUPERVISOR = 'SUPER'
    CAJERO = 'CAJERO'

    ROLES_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (SUPERVISOR, 'Supervisor'),
        (CAJERO, 'Cajero'),
    ]

    cedula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    
    rol = models.CharField(
        max_length=10,
        choices=ROLES_CHOICES,
        default=CAJERO,
        help_text="Rol asignado para el control de permisos."
    )

    # El usuario pertenece globalmente a la Empresa de Pepito
    empresa = models.ForeignKey(
        EmpresaSaaS, 
        on_delete=models.CASCADE, 
        related_name='usuarios',
        null=True, blank=True
    )

    # SUCURSALES PERMITIDAS: Relación Muchos a Muchos. 
    # El dueño puede decirle a este cajero que tiene permiso de entrar a la sucursal Norte y Sur, pero no a la Este.
    sucursales_permitidas = models.ManyToManyField(
        Parqueadero,
        blank=True,
        related_name='usuarios_permitidos',
        help_text="Sucursales a las que este usuario tiene autorización de ingresar."
    )

    def __str__(self):
        empresa_nom = self.empresa.nombre_comercial if self.empresa else "Sin Empresa"
        return f"{self.username} - {self.get_full_name()} ({empresa_nom})"