from django import forms


class BrechasBasicoForm(forms.Form):
    escenario = forms.ChoiceField(
        choices=[
            ("automatico", "Automatico por semanas"),
            ("comparativo", "Comparativo completo"),
            ("ley_100", "Panorama Ley 100"),
            ("reforma", "Panorama Reforma"),
        ],
        widget=forms.RadioSelect,
        initial="automatico",
        label="Escenario",
    )
    fecha_nacimiento = forms.DateField(
        required=False,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={"type": "date", "data-age-source": "true"}),
    )
    sexo = forms.ChoiceField(
        required=False,
        label="Genero",
        choices=[("", "Seleccione genero"), ("hombre", "Hombre"), ("mujer", "Mujer")],
    )
    edad_actual = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label="Edad actual",
        widget=forms.NumberInput(attrs={"step": "0.01", "data-age-target": "true"}),
    )
    ingreso_mensual = forms.DecimalField(max_digits=16, decimal_places=2, initial=4000000, label="Ingreso mensual objetivo")
    ibc_actual = forms.DecimalField(max_digits=16, decimal_places=2, initial=2000000, label="IBC actual")
    ibc_ultimos_10_anios = forms.DecimalField(max_digits=16, decimal_places=2, initial=2000000, label="IBC promedio 10 anos")
    anios_cotizados = forms.DecimalField(max_digits=8, decimal_places=2, initial=5, label="Anos cotizados")
    anios_por_cotizar = forms.DecimalField(max_digits=8, decimal_places=2, initial=28, label="Anos por cotizar")
    meses_cotizados_anio = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        initial=12,
        min_value=0,
        max_value=12,
        label="Meses cotizados por ano",
        widget=forms.NumberInput(attrs={"step": "1", "min": "0", "max": "12", "data-projection-control": "true"}),
        help_text="Densidad principal; el detalle tambien calcula 12, 9, 6 y 0 meses.",
    )
    capital_actual_rais = forms.DecimalField(max_digits=16, decimal_places=2, initial=0, required=False, label="Capital actual RAIS / ACCAI")
    smmlv = forms.DecimalField(max_digits=16, decimal_places=2, initial=1423500, label="SMMLV parametrizado")
    factor_capital_brecha = forms.DecimalField(max_digits=8, decimal_places=2, initial=200, label="Factor capital brecha")
    factor_capital_fedesarrollo = forms.DecimalField(max_digits=8, decimal_places=2, initial=377, label="Factor capital Fedesarrollo")
    tasa_aporte_acumulacion = forms.DecimalField(
        max_digits=7,
        decimal_places=4,
        initial="0.115",
        label="Tasa acumulacion RAIS/ACCAI",
        help_text="Supuesto editable de aporte que se acumula en cuenta individual.",
    )
    tasa_renta_mensual = forms.DecimalField(
        max_digits=7,
        decimal_places=4,
        initial="0.005",
        label="Tasa renta mensual",
        help_text="Reserva para escenarios actuariales posteriores.",
    )
