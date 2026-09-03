from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Cliente
from .services import record_timeline_event


class ClienteTests(TestCase):
    def test_timeline_records_events(self):
        user = get_user_model().objects.create_user(username="consultor")
        cliente = Cliente.objects.create(nombres="Laura", consultor=user)
        record_timeline_event(cliente=cliente, actor=user, tipo="nota", titulo="Primera llamada")
        self.assertEqual(cliente.timeline.count(), 1)

# Create your tests here.
