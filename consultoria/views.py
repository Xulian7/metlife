from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from clientes.services import record_timeline_event

from .forms import ConsultoriaCasoForm
from .models import ConsultoriaCaso


class ConsultoriaListView(LoginRequiredMixin, ListView):
    model = ConsultoriaCaso
    template_name = "consultoria/caso_list.html"
    context_object_name = "casos"


class ConsultoriaCreateView(LoginRequiredMixin, CreateView):
    model = ConsultoriaCaso
    form_class = ConsultoriaCasoForm
    template_name = "form.html"
    success_url = reverse_lazy("consultoria:list")

    def form_valid(self, form):
        form.instance.consultor = self.request.user
        response = super().form_valid(form)
        record_timeline_event(cliente=self.object.cliente, actor=self.request.user, tipo="consultoria", titulo="Diagnóstico de consultoría iniciado", descripcion=self.object.diagnostico)
        return response


class ConsultoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = ConsultoriaCaso
    form_class = ConsultoriaCasoForm
    template_name = "form.html"
    success_url = reverse_lazy("consultoria:list")

# Create your views here.
