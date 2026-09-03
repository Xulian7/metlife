from django.contrib.auth import get_user_model
from django.test import TestCase

from clientes.models import Cliente

from .models import Lead, PipelineStage
from .services import change_lead_stage, ensure_default_pipeline


class PipelineTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="consultor")
        self.cliente = Cliente.objects.create(nombres="Ana", apellidos="Perez", consultor=self.user)
        ensure_default_pipeline()

    def test_stage_change_keeps_history(self):
        nuevo = PipelineStage.objects.get(nombre="Nuevo")
        contactado = PipelineStage.objects.get(nombre="Contactado")
        lead = Lead.objects.create(cliente=self.cliente, consultor=self.user, etapa=nuevo)
        change_lead_stage(lead=lead, new_stage=contactado, actor=self.user, note="Llamada")
        lead.refresh_from_db()
        self.assertEqual(lead.etapa, contactado)
        self.assertEqual(lead.historial_etapas.count(), 1)
        self.assertEqual(self.cliente.timeline.count(), 1)

# Create your tests here.
