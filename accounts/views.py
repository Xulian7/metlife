from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import ConsultantCreateForm
from .models import ConsultantProfile


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_staff


class ConsultantListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = ConsultantProfile
    template_name = "accounts/consultant_list.html"
    context_object_name = "consultores"


class ConsultantCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = ConsultantProfile
    form_class = ConsultantCreateForm
    template_name = "form.html"
    success_url = reverse_lazy("consultores:list")

# Create your views here.
