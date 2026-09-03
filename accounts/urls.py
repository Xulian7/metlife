from django.urls import path

from . import views

app_name = "consultores"

urlpatterns = [
    path("", views.ConsultantListView.as_view(), name="list"),
    path("nuevo/", views.ConsultantCreateView.as_view(), name="create"),
]
