from django.db import models


class NormativaPensional(models.Model):
    class Estado(models.TextChoices):
        VIGENTE = "vigente", "Vigente"
        SUSPENDIDA = "suspendida", "Suspendida"
        VIGENTE_PARCIAL = "vigente_parcial", "Vigente parcialmente"
        DEROGADA = "derogada", "Derogada"
        CONDICIONADA = "condicionada", "Condicionada"
        PENDIENTE_CONTROL = "pendiente_control", "Pendiente control constitucional"
        DISCUTIBLE = "discutible", "Discutible"

    codigo = models.CharField(max_length=80, unique=True)
    nombre = models.CharField(max_length=220)
    fecha_publicacion = models.DateField(null=True, blank=True)
    fecha_inicio_efectos = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado_juridico = models.CharField(max_length=40, choices=Estado.choices)
    fuente = models.URLField(blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.codigo} - {self.get_estado_juridico_display()}"


class PensionRule(models.Model):
    normativa = models.ForeignKey(NormativaPensional, on_delete=models.CASCADE, related_name="reglas")
    code = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=40, default="borrador")
    source = models.CharField(max_length=240)
    parameters = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("normativa", "code")]

# Create your models here.
