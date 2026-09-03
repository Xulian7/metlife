from django import forms

from .models import Visita


class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        exclude = ["consultor"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "fecha_proxima_accion": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
