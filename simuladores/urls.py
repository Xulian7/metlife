from django.urls import path

from . import views

app_name = "simuladores"

urlpatterns = [
    path("", views.SimulacionListView.as_view(), name="list"),
    path("brechas/<int:cliente_id>/", views.BrechasCreateView.as_view(), name="brechas_create"),
]
