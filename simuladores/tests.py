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
        self.assertEqual(simulacion.version_motor, "0.2.0")
        self.assertEqual(simulacion.resultados_json["capital_fallecimiento"], "557120000.00")
        self.assertEqual(cliente.timeline.count(), 1)

    def test_reforma_scenario_is_stored_with_normative_warning(self):
        user = get_user_model().objects.create_user(username="consultor2")
        cliente = Cliente.objects.create(nombres="Maria", consultor=user)
        simulacion = run_excel_brechas_basico(
            cliente=cliente,
            consultor=user,
            inputs={
                "escenario": "reforma",
                "ingreso_mensual": "4000000",
                "ibc_actual": "5000000",
                "ibc_ultimos_10_anios": "4000000",
                "anios_cotizados": "10",
                "anios_por_cotizar": "20",
                "capital_actual_rais": "0",
                "smmlv": "1423500",
            },
        )
        self.assertEqual(simulacion.tipo, "brechas_panorama_reforma")
        self.assertIn("no-vigencia-plena", simulacion.normativa_version)
        self.assertEqual(simulacion.resultados_json["estado_normativo"], "Modelo consultivo no activado como regla juridica vigente plena")

# Create your tests here.
