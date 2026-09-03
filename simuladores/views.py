from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from clientes.models import Cliente

from .forms import BrechasBasicoForm
from .models import Simulacion
from .services import run_excel_brechas_basico


class SimulacionListView(LoginRequiredMixin, ListView):
    model = Simulacion
    template_name = "simuladores/simulacion_list.html"
    context_object_name = "simulaciones"


class BrechasCreateView(LoginRequiredMixin, View):
    def get(self, request, cliente_id):
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        initial = {
            "ingreso_mensual": cliente.ingresos or 4000000,
            "ibc_actual": cliente.ingresos or 2000000,
            "ibc_ultimos_10_anios": cliente.ingresos or 2000000,
        }
        return render(request, "simuladores/brechas_form.html", {"form": BrechasBasicoForm(initial=initial), "cliente": cliente})

    def post(self, request, cliente_id):
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        form = BrechasBasicoForm(request.POST)
        if form.is_valid():
            run_excel_brechas_basico(cliente=cliente, consultor=request.user, inputs=form.cleaned_data, observaciones="Motor parcial basado en BRECHAS .xlsx")
            return redirect(cliente)
        return render(request, "simuladores/brechas_form.html", {"form": form, "cliente": cliente})

# Create your views here.
