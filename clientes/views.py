from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ClienteForm, SeguimientoClienteForm
from .models import Cliente, SeguimientoCliente
from .services import change_cliente_estado, create_cliente_followup, record_timeline_event


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "clientes/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 25

    def get_queryset(self):
        qs = Cliente.objects.select_related("consultor", "fondo_pensiones", "estado_relacion").order_by("-actualizado_en")
        term = self.request.GET.get("q")
        if term:
            qs = qs.filter(Q(nombres__icontains=term) | Q(apellidos__icontains=term) | Q(numero_documento__icontains=term))
        if not self.request.user.is_staff:
            qs = qs.filter(consultor=self.request.user)
        return qs


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"

    def form_valid(self, form):
        form.instance.consultor = self.request.user
        response = super().form_valid(form)
        record_timeline_event(cliente=self.object, actor=self.request.user, tipo="cliente", titulo="Cliente creado")
        if self.object.estado_relacion:
            change_cliente_estado(cliente=self.object, new_estado=self.object.estado_relacion, actor=self.request.user, note="Estado inicial")
        return response


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs if self.request.user.is_staff else qs.filter(consultor=self.request.user)


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = "clientes/cliente_detail.html"
    context_object_name = "cliente"

    def get_queryset(self):
        qs = Cliente.objects.select_related("consultor", "fondo_pensiones", "estado_relacion").prefetch_related("timeline", "seguimientos", "simulaciones")
        return qs if self.request.user.is_staff else qs.filter(consultor=self.request.user)


class SeguimientoClienteCreateView(LoginRequiredMixin, CreateView):
    model = SeguimientoCliente
    form_class = SeguimientoClienteForm
    template_name = "form.html"
    success_url = reverse_lazy("clientes:list")

    def form_valid(self, form):
        form.instance.consultor = self.request.user
        response = super().form_valid(form)
        record_timeline_event(
            cliente=self.object.cliente,
            actor=self.request.user,
            tipo="seguimiento",
            titulo=f"Seguimiento {self.object.estado}",
            descripcion=self.object.objetivo or self.object.notas,
            object_label=self.object.tipo,
        )
        return response

# Create your views here.
