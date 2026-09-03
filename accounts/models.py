from django.conf import settings
from django.db import models


class ConsultantProfile(models.Model):
    class Role(models.TextChoices):
        ADMINISTRADOR = "administrador", "Administrador"
        DIRECTOR = "director", "Director / Supervisor"
        CONSULTOR = "consultor", "Consultor"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consultant_profile")
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.CONSULTOR)
    phone = models.CharField(max_length=40, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"

# Create your models here.
