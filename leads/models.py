from django.conf import settings
from django.db import models
from django.urls import reverse

from clientes.models import Cliente


class PipelineStage(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    orden = models.PositiveSmallIntegerField(default=0)
    activo = models.BooleanField(default=True)
    es_cierre = models.BooleanField(default=False)

    class Meta:
        ordering = ["orden", "nombre"]

    def __str__(self) -> str:
        return self.nombre


class Lead(models.Model):
    class Temperatura(models.TextChoices):
        FRIO = "frio", "Frio"
        TIBIO = "tibio", "Tibio"
        CALIENTE = "caliente", "Caliente"

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="leads")
    consultor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="leads")
    origen = models.CharField(max_length=120, blank=True)
    campana = models.CharField(max_length=120, blank=True)
    producto_interes = models.CharField(max_length=160, blank=True)
    valor_potencial = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    probabilidad = models.PositiveSmallIntegerField(default=10)
    temperatura = models.CharField(max_length=20, choices=Temperatura.choices, default=Temperatura.TIBIO)
    prioridad = models.PositiveSmallIntegerField(default=3)
    etapa = models.ForeignKey(PipelineStage, on_delete=models.PROTECT, related_name="leads")
    proximo_seguimiento = models.DateTimeField(null=True, blank=True)
    notas = models.TextField(blank=True)
    motivo_perdida = models.TextField(blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["consultor", "etapa"]), models.Index(fields=["proximo_seguimiento"])]

    def __str__(self) -> str:
        return f"{self.cliente} - {self.etapa}"

    def get_absolute_url(self):
        return reverse("leads:detail", args=[self.pk])


class LeadStageHistory(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="historial_etapas")
    from_stage = models.ForeignKey(PipelineStage, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    to_stage = models.ForeignKey(PipelineStage, on_delete=models.PROTECT, related_name="+")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]


class Seguimiento(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        REALIZADO = "realizado", "Realizado"
        VENCIDO = "vencido", "Vencido"
        CANCELADO = "cancelado", "Cancelado"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="seguimientos")
    consultor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=60, default="llamada")
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    notas = models.TextField(blank=True)
    resultado = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha"]

# Create your models here.
