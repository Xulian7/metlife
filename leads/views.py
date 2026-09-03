from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from clientes.services import record_timeline_event

from .forms import LeadForm, SeguimientoForm
from .models import Lead, Seguimiento
from .services import change_lead_stage


class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        qs = Lead.objects.select_related("cliente", "consultor", "etapa").order_by("etapa__orden", "-actualizado_en")
        return qs if self.request.user.is_staff else qs.filter(consultor=self.request.user)


class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.consultor = self.request.user
        response = super().form_valid(form)
        change_lead_stage(lead=self.object, new_stage=self.object.etapa, actor=self.request.user, note="Creacion del lead")
        return response


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = "form.html"

    def form_valid(self, form):
        previous = Lead.objects.get(pk=self.object.pk)
        response = super().form_valid(form)
        if previous.etapa_id != self.object.etapa_id:
            change_lead_stage(lead=self.object, new_stage=self.object.etapa, actor=self.request.user, note="Cambio desde formulario")
        return response


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        return Lead.objects.select_related("cliente", "etapa", "consultor").prefetch_related("historial_etapas")


class SeguimientoCreateView(LoginRequiredMixin, CreateView):
    model = Seguimiento
    form_class = SeguimientoForm
    template_name = "form.html"
    success_url = reverse_lazy("leads:list")

    def form_valid(self, form):
        form.instance.consultor = self.request.user
        response = super().form_valid(form)
        record_timeline_event(cliente=self.object.lead.cliente, actor=self.request.user, tipo="seguimiento", titulo=f"Seguimiento {self.object.estado}", descripcion=self.object.notas, object_label=self.object.tipo)
        return response

# Create your views here.
