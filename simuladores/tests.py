from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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
                "escenario": "ley_100",
                "ingreso_mensual": "4000000",
                "ibc_actual": "2000000",
                "ibc_ultimos_10_anios": "2000000",
                "anios_cotizados": "5",
                "anios_por_cotizar": "28",
                "smmlv": "1423500",
            },
        )
        self.assertEqual(simulacion.version_motor, "0.4.0")
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
        self.assertEqual(simulacion.resultados_json["estado_normativo"], "Modelo consultivo no activado como regla jurídica vigente plena")

    def test_default_comparative_scenario_stores_tables_and_detail_page(self):
        user = get_user_model().objects.create_user(username="consultor3", password="clave")
        cliente = Cliente.objects.create(nombres="Andrea", sexo="mujer", consultor=user)
        simulacion = run_excel_brechas_basico(
            cliente=cliente,
            consultor=user,
            inputs={
                "escenario": "comparativo",
                "ingreso_mensual": "4000000",
                "ibc_actual": "3000000",
                "ibc_ultimos_10_anios": "2800000",
                "anios_cotizados": "12",
                "anios_por_cotizar": "18",
                "meses_cotizados_anio": "9",
                "smmlv": "1423500",
            },
        )
        self.assertEqual(simulacion.tipo, "brechas_pensional_comparativo")
        self.assertIn("ley_100", simulacion.resultados_json)
        self.assertIn("reforma", simulacion.resultados_json)
        self.assertEqual(len(simulacion.resultados_json["proyecciones"]), 4)
        self.client.force_login(user)
        response = self.client.get(reverse("simuladores:detail", args=[simulacion.pk]), follow=True)
        self.assertContains(response, "Proyección por densidad de cotización")
        self.assertContains(response, "Panorama Ley 100")
        self.assertContains(response, "$ 4.000.000")
        self.assertNotContains(response, "$ 4.000.000,00")

    def test_automatic_scenario_uses_transition_threshold(self):
        user = get_user_model().objects.create_user(username="consultor4")
        cliente = Cliente.objects.create(nombres="Jorge", sexo="hombre", consultor=user)
        simulacion = run_excel_brechas_basico(
            cliente=cliente,
            consultor=user,
            inputs={
                "escenario": "automatico",
                "ingreso_mensual": "4000000",
                "ibc_actual": "3000000",
                "ibc_ultimos_10_anios": "2800000",
                "anios_cotizados": "17.3076923077",
                "anios_por_cotizar": "12",
                "smmlv": "1423500",
            },
        )
        self.assertEqual(simulacion.tipo, "brechas_regimen_automatico")
        self.assertEqual(simulacion.resultados_json["regimen_aplicado"], "Ley 100 / Ley 797")
        self.assertTrue(simulacion.resultados_json["contexto"]["cumple_regimen_transicion_ley_2381"])

# Create your tests here.
