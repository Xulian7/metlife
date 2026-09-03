from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("", views.LeadListView.as_view(), name="list"),
    path("nuevo/", views.LeadCreateView.as_view(), name="create"),
    path("<int:pk>/", views.LeadDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", views.LeadUpdateView.as_view(), name="update"),
    path("seguimientos/nuevo/", views.SeguimientoCreateView.as_view(), name="seguimiento_create"),
]
