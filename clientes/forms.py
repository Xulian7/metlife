from django import forms

from .models import Cliente, Consentimiento


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "tipo_persona", "tipo_documento", "numero_documento", "nombres", "apellidos",
            "fecha_nacimiento", "sexo", "estado_civil", "ciudad", "direccion", "telefono",
            "whatsapp", "email", "ocupacion", "empresa", "cargo", "origen", "segmento",
            "estado", "etiquetas", "ingresos", "ingresos_adicionales", "gastos_estimados",
            "activos", "pasivos", "personas_a_cargo", "capacidad_ahorro",
            "proxima_accion", "proxima_accion_fecha",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "proxima_accion_fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ConsentimientoForm(forms.ModelForm):
    class Meta:
        model = Consentimiento
        fields = ["finalidad", "autorizado", "fecha_autorizacion", "fuente", "evidencia"]
        widgets = {"fecha_autorizacion": forms.DateTimeInput(attrs={"type": "datetime-local"})}
