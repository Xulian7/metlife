from django import forms


class BrechasBasicoForm(forms.Form):
    ingreso_mensual = forms.DecimalField(max_digits=16, decimal_places=2, initial=4000000)
    ibc_actual = forms.DecimalField(max_digits=16, decimal_places=2, initial=2000000)
    ibc_ultimos_10_anios = forms.DecimalField(max_digits=16, decimal_places=2, initial=2000000)
    anios_cotizados = forms.DecimalField(max_digits=8, decimal_places=2, initial=5)
    anios_por_cotizar = forms.DecimalField(max_digits=8, decimal_places=2, initial=28)
    smmlv = forms.DecimalField(max_digits=16, decimal_places=2, initial=1423500)
