from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from django.views.generic import TemplateView

from clientes.models import Cliente
from leads.models import Lead, Seguimiento
from simuladores.models import Simulacion
from visitas.models import Visita


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()
        leads = Lead.objects.select_related("etapa")
        visitas = Visita.objects.select_related("cliente")
        seguimientos = Seguimiento.objects.select_related("lead", "lead__cliente")
        if not self.request.user.is_staff:
            leads = leads.filter(consultor=self.request.user)
            visitas = visitas.filter(consultor=self.request.user)
            seguimientos = seguimientos.filter(consultor=self.request.user)
        ctx.update(
            clientes_total=Cliente.objects.count() if self.request.user.is_staff else Cliente.objects.filter(consultor=self.request.user).count(),
            leads_activos=leads.exclude(etapa__es_cierre=True).count(),
            leads_nuevos=leads.filter(etapa__nombre="Nuevo").count(),
            citas_proximas=visitas.filter(fecha__gte=today).count(),
            visitas_mes=visitas.filter(fecha__year=today.year, fecha__month=today.month).count(),
            seguimientos_hoy=seguimientos.filter(fecha__date=today).count(),
            seguimientos_vencidos=seguimientos.filter(fecha__date__lt=today, estado="pendiente").count(),
            simulaciones=Simulacion.objects.count(),
            pipeline=leads.values("etapa__nombre").annotate(total=Count("id")).order_by("etapa__orden"),
            proximos_seguimientos=seguimientos.order_by("fecha")[:8],
            ultimas_visitas=visitas.order_by("-fecha")[:8],
        )
        return ctx

# Create your views here.
