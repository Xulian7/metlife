from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from decimal import Decimal, InvalidOperation

from clientes.models import Cliente
from pensiones.services import PENSION_GLOSSARY

from .forms import BrechasBasicoForm
from .models import Simulacion
from .services import run_excel_brechas_basico


class SimulacionListView(LoginRequiredMixin, ListView):
    model = Simulacion
    template_name = "simuladores/simulacion_list.html"
    context_object_name = "simulaciones"

    def get_queryset(self):
        return super().get_queryset().select_related("cliente", "consultor")


def labelize(key: str) -> str:
    labels = {
        "anio": "Año",
        "anios": "Años",
        "ibc_ultimos_10_anios": "IBC promedio 10 años",
        "edad_requisito_rpm": "Edad requisito RPM",
        "semanas_requeridas_transicion_ley_2381": "Semanas requeridas transición Ley 2381",
        "cumple_regimen_transicion_ley_2381": "Cumple régimen de transición Ley 2381",
        "regimen_simulacion_recomendado": "Régimen de simulación recomendado",
        "fundamento_decision_regimen": "Fundamento de decisión de régimen",
        "regimen_aplicado": "Régimen aplicado",
        "estado_normativo": "Estado normativo",
        "pension_vejez_rpm_ley_100": "Pensión vejez RPM Ley 100",
        "pension_vejez_rais_ley_100": "Pensión vejez RAIS Ley 100",
        "pension_total_reforma": "Pensión total Reforma",
        "brecha_menor_vejez": "Brecha menor de vejez",
        "tasa_aporte_acumulacion": "Tasa acumulación RAIS/ACCAI",
    }
    return labels.get(key, key.replace("_", " ").capitalize())


MONEY_KEYS = {
    "ingreso_mensual",
    "ibc_actual",
    "ibc_ultimos_10_anios",
    "smmlv",
    "minimo_neto",
    "capital_fedesarrollo",
    "capital_actual_rais",
    "acumulacion_proyectada_rais",
    "acumulacion_proyectada_accai",
    "ibc_colpensiones",
    "ibc_accai",
    "pension_invalidez",
    "pension_sobrevivencia",
    "pension_colpensiones",
    "pension_privada",
    "pension_accai",
    "pension_total_sistema",
    "pension_vejez_rpm_ley_100",
    "pension_vejez_rais_ley_100",
    "pension_total_reforma",
    "pension_rpm_estimada",
    "pension_rais_estimada",
    "brecha_fallecimiento",
    "brecha_invalidez",
    "brecha_vejez_colpensiones",
    "brecha_vejez_privada",
    "brecha_vejez_sistema",
    "brecha_menor_vejez",
    "capital_fallecimiento",
    "capital_invalidez",
    "capital_vejez_colpensiones",
    "capital_vejez_privada",
    "capital_vejez_sistema",
}
PERCENT_KEYS = {"tasa_aporte_acumulacion", "tasa_renta_mensual", "tasa_descuento_neto_ley_100", "tasa_descuento_neto_reforma"}


def as_decimal(value) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def money_label(value) -> str:
    amount = as_decimal(value)
    if amount is None:
        return value_label(value)
    rounded = int(amount.quantize(Decimal("1")))
    sign = "-" if rounded < 0 else ""
    formatted = f"{abs(rounded):,}".replace(",", ".")
    return f"{sign}$ {formatted}"


def percent_label(value) -> str:
    number = as_decimal(value)
    if number is None:
        return value_label(value)
    return f"{(number * Decimal('100')).quantize(Decimal('0.01'))}%"


def value_label(value) -> str:
    if value is True:
        return "Sí"
    if value is False:
        return "No"
    if value in (None, ""):
        return "Sin dato"
    return str(value)


def formatted_value(key: str, value) -> str:
    if key in MONEY_KEYS:
        return money_label(value)
    if key in PERCENT_KEYS:
        return percent_label(value)
    return value_label(value)


def table_rows(data: dict | None, *, exclude: set[str] | None = None) -> list[dict]:
    exclude = exclude or set()
    rows = []
    for key, value in (data or {}).items():
        if key in exclude or isinstance(value, (dict, list)):
            continue
        rows.append({"label": labelize(key), "value": formatted_value(key, value), "is_money": key in MONEY_KEYS})
    return rows


def projection_rows(rows: list[dict] | None) -> list[dict]:
    formatted = []
    for row in rows or []:
        formatted.append(
            {
                "cotiza_meses_anio": value_label(row.get("cotiza_meses_anio")),
                "semanas_proyectadas": value_label(row.get("semanas_proyectadas")),
                "edad_estimada_pension_rpm": value_label(row.get("edad_estimada_pension_rpm")),
                "cumple_rpm": value_label(row.get("cumple_rpm")),
                "cumple_garantia_rais": value_label(row.get("cumple_garantia_rais")),
                "pension_rpm_estimada": money_label(row.get("pension_rpm_estimada")),
                "pension_rais_estimada": money_label(row.get("pension_rais_estimada")),
            }
        )
    return formatted


class SimulacionDetailView(LoginRequiredMixin, DetailView):
    model = Simulacion
    template_name = "simuladores/simulacion_detail.html"
    context_object_name = "simulacion"

    def get_queryset(self):
        return super().get_queryset().select_related("cliente", "consultor")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resultados = self.object.resultados_json or {}
        exclude = {"engine_version", "ruleset_version", "contexto"}
        regimen_aplicado = resultados.get("regimen_aplicado", "")
        is_reforma_result = self.object.tipo == "brechas_panorama_reforma" or str(regimen_aplicado).startswith("Reforma")
        ley100_source = resultados.get("ley_100") or (None if is_reforma_result else resultados)
        reforma_source = resultados.get("reforma") or (resultados if is_reforma_result else None)
        context.update(
            {
                "resumen_rows": table_rows(resultados.get("resumen") or resultados.get("contexto"), exclude=exclude),
                "contexto_rows": table_rows(resultados.get("contexto"), exclude=exclude),
                "comparison_rows": table_rows(resultados.get("comparacion"), exclude=exclude),
                "ley100_rows": table_rows(ley100_source, exclude=exclude),
                "reforma_rows": table_rows(reforma_source, exclude=exclude),
                "projection_rows": projection_rows(resultados.get("proyecciones", [])),
                "alerts": resultados.get("alertas", []),
                "sources": resultados.get("fuentes", []),
                "glossary": PENSION_GLOSSARY,
                "inputs_rows": table_rows(self.object.inputs_json),
            }
        )
        return context


class BrechasCreateView(LoginRequiredMixin, View):
    def get(self, request, cliente_id):
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        initial = {
            "fecha_nacimiento": cliente.fecha_nacimiento,
            "sexo": cliente.sexo,
            "edad_actual": cliente.edad,
            "ingreso_mensual": cliente.ingresos or 4000000,
            "ibc_actual": cliente.ingresos or 2000000,
            "ibc_ultimos_10_anios": cliente.ingresos or 2000000,
        }
        return render(request, "simuladores/brechas_form.html", {"form": BrechasBasicoForm(initial=initial), "cliente": cliente})

    def post(self, request, cliente_id):
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        form = BrechasBasicoForm(request.POST)
        if form.is_valid():
            simulacion = run_excel_brechas_basico(cliente=cliente, consultor=request.user, inputs=form.cleaned_data, observaciones="Motor basado en BRECHAS .xlsx con proyecciones pensionales")
            return redirect(simulacion)
        return render(request, "simuladores/brechas_form.html", {"form": form, "cliente": cliente})

# Create your views here.
