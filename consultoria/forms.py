from django import forms

from .models import ConsultoriaCaso


class ConsultoriaCasoForm(forms.ModelForm):
    class Meta:
        model = ConsultoriaCaso
        fields = ["cliente", "visita", "estado", "diagnostico", "oportunidades", "proximos_pasos"]
