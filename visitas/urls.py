from django.urls import path

from . import views

app_name = "visitas"

urlpatterns = [
    path("", views.VisitaListView.as_view(), name="list"),
    path("nueva/", views.VisitaCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", views.VisitaUpdateView.as_view(), name="update"),
]
