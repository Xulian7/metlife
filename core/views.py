from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from django.views.generic import TemplateView

from clientes.models import Cliente
from clientes.models import SeguimientoCliente
from simuladores.models import Simulacion
from visitas.models import Visita


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()
        visitas = Visita.objects.select_related("cliente")
        clientes = Cliente.objects.select_related("estado_relacion", "fondo_pensiones")
        seguimientos = SeguimientoCliente.objects.select_related("cliente")
        if not self.request.user.is_staff:
            clientes = clientes.filter(consultor=self.request.user)
            visitas = visitas.filter(consultor=self.request.user)
            seguimientos = seguimientos.filter(consultor=self.request.user)
        ctx.update(
            clientes_total=clientes.count(),
            clientes_nuevos=clientes.filter(estado_relacion__nombre="Nuevo").count(),
            clientes_activos=clientes.filter(estado_relacion__nombre__in=["Seguimiento activo", "Cliente activo", "Diagnostico en curso"]).count(),
            citas_proximas=visitas.filter(fecha__gte=today).count(),
            visitas_mes=visitas.filter(fecha__year=today.year, fecha__month=today.month).count(),
            seguimientos_hoy=seguimientos.filter(fecha__date=today).count(),
            seguimientos_vencidos=seguimientos.filter(fecha__date__lt=today, estado="pendiente").count(),
            simulaciones=Simulacion.objects.count(),
            pipeline=clientes.values("estado_relacion__nombre").annotate(total=Count("id")).order_by("estado_relacion__orden"),
            proximos_seguimientos=seguimientos.order_by("fecha")[:8],
            ultimas_visitas=visitas.order_by("-fecha")[:8],
        )
        return ctx

# Create your views here.
