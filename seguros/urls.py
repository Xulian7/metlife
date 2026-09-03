from django.urls import path

from .views import DiagnosticoProteccionListView

app_name = "seguros"

urlpatterns = [path("", DiagnosticoProteccionListView.as_view(), name="list")]
