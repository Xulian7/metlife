from django.contrib.auth import get_user_model
from django.test import TestCase

from clientes.models import Cliente

from .services import run_excel_brechas_basico


class SimuladorPersistenceTests(TestCase):
    def test_simulation_stores_inputs_outputs_and_versions(self):
        user = get_user_model().objects.create_user(username="consultor")
        cliente = Cliente.objects.create(nombres="Carlos", consultor=user)
        simulacion = run_excel_brechas_basico(
            cliente=cliente,
            consultor=user,
            inputs={
                "ingreso_mensual": "4000000",
                "ibc_actual": "2000000",
                "ibc_ultimos_10_anios": "2000000",
                "anios_cotizados": "5",
                "anios_por_cotizar": "28",
                "smmlv": "1423500",
            },
        )
        self.assertEqual(simulacion.version_motor, "0.1.0")
        self.assertEqual(simulacion.resultados_json["capital_fallecimiento"], "557120000.00")
        self.assertEqual(cliente.timeline.count(), 1)

# Create your tests here.
