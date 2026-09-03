from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView

from clientes.services import record_timeline_event

from .forms import VisitaForm
from .models import Visita


class VisitaListView(LoginRequiredMixin, ListView):
    model = Visita
    template_name = "visitas/visita_list.html"
    context_object_name = "visitas"

    def get_queryset(self):
        qs = Visita.objects.select_related("cliente", "consultor")
        return qs if self.request.user.is_staff else qs.filter(consultor=self.request.user)


class VisitaCreateView(LoginRequiredMixin, CreateView):
    model = Visita
    form_class = VisitaForm
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.consultor = self.request.user
        response = super().form_valid(form)
        record_timeline_event(cliente=self.object.cliente, actor=self.request.user, tipo="visita", titulo=f"Visita {self.object.estado}", descripcion=self.object.objetivo, object_label=str(self.object.fecha))
        return response


class VisitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Visita
    form_class = VisitaForm
    template_name = "form.html"

# Create your views here.
