from django.contrib.auth import get_user_model
from django.test import TestCase

from .forms import ClienteForm
from .models import Cliente, ClienteEstado, SeguimientoCliente
from .services import change_cliente_estado, create_cliente_followup, record_timeline_event


class ClienteTests(TestCase):
    def test_timeline_records_events(self):
        user = get_user_model().objects.create_user(username="consultor")
        cliente = Cliente.objects.create(nombres="Laura", consultor=user)
        record_timeline_event(cliente=cliente, actor=user, tipo="nota", titulo="Primera llamada")
        self.assertEqual(cliente.timeline.count(), 1)

    def test_cliente_form_stores_children_ages(self):
        user = get_user_model().objects.create_user(username="consultor2")
        estado = ClienteEstado.objects.get(nombre="Nuevo")
        form = ClienteForm(
            data={
                "tipo_persona": "natural",
                "tipo_documento": "CC",
                "numero_documento": "123",
                "nombres": "Andrea",
                "apellidos": "Lopez",
                "fecha_nacimiento": "1990-01-15",
                "sexo": "F",
                "estado_civil": "Casada",
                "estado_relacion": estado.id,
                "estado": "prospecto",
                "personas_a_cargo": 3,
                "tiene_conyuge": "on",
                "conyuge_nombre": "Juan",
                "conyuge_fecha_nacimiento": "1989-05-01",
                "numero_hijos": 2,
                "hijos_edades": "8, 12",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        cliente = form.save(commit=False)
        cliente.consultor = user
        cliente.save()
        self.assertEqual(cliente.numero_hijos, 2)
        self.assertEqual(cliente.hijos, [{"edad": 8}, {"edad": 12}])

    def test_cliente_state_and_followup_record_timeline(self):
        user = get_user_model().objects.create_user(username="consultor3")
        estado = ClienteEstado.objects.get(nombre="Visitado")
        cliente = Cliente.objects.create(nombres="Laura", consultor=user)
        change_cliente_estado(cliente=cliente, new_estado=estado, actor=user, note="Primera reunion")
        create_cliente_followup(cliente=cliente, consultor=user, fecha="2026-09-04T09:00:00-05:00", tipo="reunion", objetivo="Revisar simulacion")
        self.assertEqual(cliente.historial_estados.count(), 1)
        self.assertEqual(SeguimientoCliente.objects.filter(cliente=cliente).count(), 1)
        self.assertEqual(cliente.timeline.count(), 2)

# Create your tests here.
