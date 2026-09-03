from django.conf import settings
from django.db import models

from clientes.models import Cliente
from visitas.models import Visita


class ConsultoriaCaso(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        EN_DIAGNOSTICO = "diagnostico", "Diagnostico"
        CERRADO = "cerrado", "Cerrado"

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="consultorias")
    visita = models.ForeignKey(Visita, on_delete=models.SET_NULL, null=True, blank=True, related_name="consultorias")
    consultor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.BORRADOR)
    datos_personales = models.JSONField(default=dict, blank=True)
    situacion_laboral = models.JSONField(default=dict, blank=True)
    informacion_economica = models.JSONField(default=dict, blank=True)
    informacion_pensional = models.JSONField(default=dict, blank=True)
    historia_cotizacion = models.JSONField(default=dict, blank=True)
    familia_dependientes = models.JSONField(default=dict, blank=True)
    coberturas_actuales = models.JSONField(default=dict, blank=True)
    objetivos = models.JSONField(default=dict, blank=True)
    diagnostico = models.TextField(blank=True)
    oportunidades = models.TextField(blank=True)
    proximos_pasos = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Consultoria {self.cliente} ({self.estado})"

# Create your models here.
