from django.urls import path

from . import views

app_name = "consultoria"

urlpatterns = [
    path("", views.ConsultoriaListView.as_view(), name="list"),
    path("nueva/", views.ConsultoriaCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", views.ConsultoriaUpdateView.as_view(), name="update"),
]
