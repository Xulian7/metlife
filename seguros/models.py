from decimal import Decimal

from django.conf import settings
from django.db import models

from clientes.models import Cliente


class DiagnosticoProteccion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="diagnosticos_proteccion")
    consultor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    necesidad_fallecimiento = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    necesidad_invalidez = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    necesidad_educacion = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    cobertura_existente = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    parametros = models.JSONField(default=dict, blank=True)
    conclusiones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    @property
    def necesidad_total(self) -> Decimal:
        return self.necesidad_fallecimiento + self.necesidad_invalidez + self.necesidad_educacion

    @property
    def brecha_proteccion(self) -> Decimal:
        return self.necesidad_total - self.cobertura_existente


class CoberturaExistente(models.Model):
    diagnostico = models.ForeignKey(DiagnosticoProteccion, on_delete=models.CASCADE, related_name="coberturas")
    tipo = models.CharField(max_length=80)
    proveedor = models.CharField(max_length=160, blank=True)
    valor_asegurado = models.DecimalField(max_digits=16, decimal_places=2)
    vigencia_hasta = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

# Create your models here.
