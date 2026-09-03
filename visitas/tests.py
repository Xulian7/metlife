from django.contrib.auth import get_user_model
from django.test import TestCase

from clientes.models import Cliente

from .models import Visita


class VisitaModelTests(TestCase):
    def test_create_visit(self):
        user = get_user_model().objects.create_user(username="consultor")
        cliente = Cliente.objects.create(nombres="Carlos", consultor=user)
        visita = Visita.objects.create(cliente=cliente, consultor=user, fecha="2026-09-02", objetivo="Diagnostico")
        self.assertEqual(str(visita), "Carlos - 2026-09-02")

# Create your tests here.
