from django import forms

from .models import Lead, Seguimiento


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["cliente", "origen", "campana", "producto_interes", "valor_potencial", "probabilidad", "temperatura", "prioridad", "etapa", "proximo_seguimiento", "notas", "motivo_perdida", "fecha_cierre"]
        widgets = {
            "proximo_seguimiento": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fecha_cierre": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento
        fields = ["lead", "fecha", "tipo", "estado", "notas", "resultado"]
        widgets = {"fecha": forms.DateTimeInput(attrs={"type": "datetime-local"})}
