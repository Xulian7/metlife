from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import DiagnosticoProteccion


class DiagnosticoProteccionListView(LoginRequiredMixin, ListView):
    model = DiagnosticoProteccion
    template_name = "seguros/diagnostico_list.html"
    context_object_name = "diagnosticos"

# Create your views here.
