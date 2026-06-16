from django.db import models
from django.utils import timezone


class RegistroAcceso(models.Model):
    RESULTADO_CHOICES = [
        ('EXITOSO', 'Exitoso'),
        ('FALLIDO', 'Fallido'),
        ('BLOQUEADO', 'Bloqueado'),
    ]

    usuario_texto = models.CharField(
        max_length=150,
        help_text="Username o correo ingresado"
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    resultado = models.CharField(
        max_length=10,
        choices=RESULTADO_CHOICES,
        default='FALLIDO'
    )
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Registro de acceso"
        verbose_name_plural = "Registros de acceso"

    def __str__(self):
        return f"{self.usuario_texto} | {self.resultado} | {self.fecha:%d/%m/%Y %H:%M}"