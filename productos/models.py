from django.db import models


class Producto(models.Model):
    categoria = models.CharField(max_length=80)
    nombre = models.CharField(max_length=160)
    proveedor = models.CharField(max_length=160, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    caracteristicas = models.JSONField(default=dict, blank=True)
    requisitos = models.TextField(blank=True)
    documentacion = models.TextField(blank=True)
    parametros = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["categoria", "nombre"]

    def __str__(self) -> str:
        return f"{self.categoria} - {self.nombre}"

# Create your models here.
