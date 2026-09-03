from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Cliente(models.Model):
    class TipoPersona(models.TextChoices):
        NATURAL = "natural", "Natural"
        JURIDICA = "juridica", "Juridica"

    class Estado(models.TextChoices):
        PROSPECTO = "prospecto", "Prospecto"
        ACTIVO = "activo", "Cliente activo"
        INACTIVO = "inactivo", "Inactivo"

    tipo_persona = models.CharField(max_length=20, choices=TipoPersona.choices, default=TipoPersona.NATURAL)
    tipo_documento = models.CharField(max_length=20, blank=True)
    numero_documento = models.CharField(max_length=40, blank=True, db_index=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=20, blank=True)
    estado_civil = models.CharField(max_length=40, blank=True)
    ciudad = models.CharField(max_length=120, blank=True)
    direccion = models.CharField(max_length=240, blank=True)
    telefono = models.CharField(max_length=40, blank=True)
    whatsapp = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    ocupacion = models.CharField(max_length=150, blank=True)
    empresa = models.CharField(max_length=150, blank=True)
    cargo = models.CharField(max_length=150, blank=True)
    consultor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="clientes")
    origen = models.CharField(max_length=120, blank=True)
    segmento = models.CharField(max_length=120, blank=True)
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.PROSPECTO)
    etiquetas = models.CharField(max_length=250, blank=True)
    ingresos = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    ingresos_adicionales = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    gastos_estimados = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    activos = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    pasivos = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    personas_a_cargo = models.PositiveSmallIntegerField(default=0)
    capacidad_ahorro = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    ultima_interaccion = models.DateTimeField(null=True, blank=True)
    proxima_accion = models.CharField(max_length=180, blank=True)
    proxima_accion_fecha = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["consultor", "estado"]), models.Index(fields=["numero_documento"])]
        constraints = [
            models.UniqueConstraint(
                fields=["tipo_documento", "numero_documento"],
                condition=~models.Q(numero_documento=""),
                name="unique_cliente_documento_no_vacio",
            )
        ]

    def __str__(self) -> str:
        return self.nombre_completo

    @property
    def nombre_completo(self) -> str:
        return " ".join(part for part in [self.nombres, self.apellidos] if part).strip()

    @property
    def edad(self) -> int | None:
        if not self.fecha_nacimiento:
            return None
        today = timezone.localdate()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def get_absolute_url(self):
        return reverse("clientes:detail", args=[self.pk])


class Consentimiento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="consentimientos")
    finalidad = models.TextField()
    autorizado = models.BooleanField(default=False)
    fecha_autorizacion = models.DateTimeField(null=True, blank=True)
    fuente = models.CharField(max_length=120, blank=True)
    evidencia = models.FileField(upload_to="consentimientos/", blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    creado_en = models.DateTimeField(auto_now_add=True)


class TimelineEvent(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="timeline")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=60)
    titulo = models.CharField(max_length=180)
    descripcion = models.TextField(blank=True)
    object_label = models.CharField(max_length=180, blank=True)
    occurred_at = models.DateTimeField(default=timezone.now, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-occurred_at", "-id"]

    def __str__(self) -> str:
        return f"{self.cliente} - {self.titulo}"

# Create your models here.
