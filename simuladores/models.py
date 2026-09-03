from django.conf import settings
from django.db import models
from django.urls import reverse

from clientes.models import Cliente


class Simulacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="simulaciones")
    consultor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=80)
    version_motor = models.CharField(max_length=40)
    inputs_json = models.JSONField()
    resultados_json = models.JSONField()
    normativa_version = models.CharField(max_length=120)
    observaciones = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["-fecha"]
        indexes = [models.Index(fields=["cliente", "tipo", "fecha"])]

    def __str__(self) -> str:
        return f"{self.tipo} - {self.cliente} - {self.fecha:%Y-%m-%d}"

    @property
    def tipo_label(self) -> str:
        labels = {
            "brechas_regimen_automatico": "Automático por semanas",
            "brechas_pensional_comparativo": "Comparativo pensional",
            "brechas_panorama_ley_100": "Panorama Ley 100",
            "brechas_panorama_reforma": "Panorama Reforma",
        }
        return labels.get(self.tipo, self.tipo.replace("_", " ").capitalize())

    def get_absolute_url(self):
        return reverse("simuladores:detail", args=[self.pk])

# Create your models here.
