from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from clientes.models import Cliente

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


def value_label(value) -> str:
    if value is True:
        return "Si"
    if value is False:
        return "No"
    if value in (None, ""):
        return "Sin dato"
    return str(value)


def table_rows(data: dict | None, *, exclude: set[str] | None = None) -> list[dict]:
    exclude = exclude or set()
    rows = []
    for key, value in (data or {}).items():
        if key in exclude or isinstance(value, (dict, list)):
            continue
        rows.append({"label": labelize(key), "value": value_label(value)})
    return rows


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
                "projection_rows": resultados.get("proyecciones", []),
                "alerts": resultados.get("alertas", []),
                "sources": resultados.get("fuentes", []),
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
