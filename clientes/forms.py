from django import forms

from .models import Cliente, Consentimiento, SeguimientoCliente


class ClienteForm(forms.ModelForm):
    hijos_edades = forms.CharField(
        label="Edades de hijos",
        required=False,
        help_text="Separe las edades con comas. Ejemplo: 8, 12, 16.",
    )

    class Meta:
        model = Cliente
        fields = [
            "tipo_persona", "tipo_documento", "numero_documento", "nombres", "apellidos",
            "fecha_nacimiento", "fondo_pensiones", "sexo", "estado_civil", "estado_relacion", "ciudad", "direccion", "telefono",
            "whatsapp", "email", "ocupacion", "empresa", "cargo", "origen", "segmento",
            "estado", "etiquetas", "ingresos", "ingresos_adicionales", "gastos_estimados",
            "activos", "pasivos", "personas_a_cargo", "tiene_conyuge", "conyuge_nombre",
            "conyuge_fecha_nacimiento", "numero_hijos", "hijos_edades", "capacidad_ahorro",
            "proxima_accion", "proxima_accion_fecha",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "conyuge_fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "proxima_accion_fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fondo_pensiones"].empty_label = "Seleccione fondo pensional"
        self.fields["estado_relacion"].empty_label = "Seleccione estado"
        if not self.instance.pk:
            from .models import ClienteEstado

            first_state = ClienteEstado.objects.filter(activo=True).order_by("orden").first()
            if first_state:
                self.fields["estado_relacion"].initial = first_state
        if self.instance and self.instance.pk and self.instance.hijos:
            self.fields["hijos_edades"].initial = ", ".join(str(hijo.get("edad", "")) for hijo in self.instance.hijos if hijo.get("edad") != "")

    def clean_hijos_edades(self):
        value = self.cleaned_data.get("hijos_edades", "")
        if not value.strip():
            return []
        edades = []
        for raw in value.replace(";", ",").split(","):
            raw = raw.strip()
            if not raw:
                continue
            try:
                edad = int(raw)
            except ValueError as exc:
                raise forms.ValidationError("Las edades de hijos deben ser numeros separados por comas.") from exc
            if edad < 0 or edad > 100:
                raise forms.ValidationError("Revise las edades de hijos; deben estar entre 0 y 100.")
            edades.append({"edad": edad})
        return edades

    def save(self, commit=True):
        instance = super().save(commit=False)
        hijos = self.cleaned_data.get("hijos_edades", [])
        instance.hijos = hijos
        instance.numero_hijos = len(hijos) if hijos else instance.numero_hijos
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class ConsentimientoForm(forms.ModelForm):
    class Meta:
        model = Consentimiento
        fields = ["finalidad", "autorizado", "fecha_autorizacion", "fuente", "evidencia"]
        widgets = {"fecha_autorizacion": forms.DateTimeInput(attrs={"type": "datetime-local"})}


class SeguimientoClienteForm(forms.ModelForm):
    class Meta:
        model = SeguimientoCliente
        fields = ["cliente", "fecha", "tipo", "objetivo", "estado", "notas", "resultado"]
        widgets = {"fecha": forms.DateTimeInput(attrs={"type": "datetime-local"})}
