from django.conf import settings
from django.db import models
from django.urls import reverse

from clientes.models import Cliente


class Visita(models.Model):
    class Estado(models.TextChoices):
        PROGRAMADA = "programada", "Programada"
        CONFIRMADA = "confirmada", "Confirmada"
        REALIZADA = "realizada", "Realizada"
        CANCELADA = "cancelada", "Cancelada"
        REPROGRAMADA = "reprogramada", "Reprogramada"
        NO_ASISTIO = "no_asistio", "No asistio"

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="visitas")
    consultor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="visitas")
    fecha = models.DateField()
    hora = models.TimeField(null=True, blank=True)
    modalidad = models.CharField(max_length=60, default="Presencial")
    ubicacion = models.CharField(max_length=240, blank=True)
    objetivo = models.CharField(max_length=220, blank=True)
    motivo = models.TextField(blank=True)
    asistentes = models.TextField(blank=True)
    situacion_actual = models.TextField(blank=True)
    necesidades_detectadas = models.TextField(blank=True)
    informacion_recopilada = models.JSONField(default=dict, blank=True)
    productos_discutidos = models.TextField(blank=True)
    simulaciones_realizadas = models.TextField(blank=True)
    conclusiones = models.TextField(blank=True)
    compromisos_cliente = models.TextField(blank=True)
    compromisos_consultor = models.TextField(blank=True)
    proxima_accion = models.CharField(max_length=180, blank=True)
    fecha_proxima_accion = models.DateTimeField(null=True, blank=True)
    observaciones_privadas = models.TextField(blank=True)
    archivo_adjunto = models.FileField(upload_to="visitas/", blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PROGRAMADA)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha", "-hora"]
        indexes = [models.Index(fields=["consultor", "fecha"]), models.Index(fields=["cliente", "fecha"])]

    def __str__(self) -> str:
        return f"{self.cliente} - {self.fecha}"

    def get_absolute_url(self):
        return reverse("clientes:detail", args=[self.cliente_id])

# Create your models here.
