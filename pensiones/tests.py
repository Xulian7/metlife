from decimal import Decimal

from django.test import TestCase

from .services import PensionInputs, calcular_panorama_ley_100


class PensionEngineTests(TestCase):
    def test_excel_brechas_ley_100_main_case(self):
        result = calcular_panorama_ley_100(
            PensionInputs(
                ingreso_mensual=Decimal("4000000"),
                ibc_actual=Decimal("2000000"),
                ibc_ultimos_10_anios=Decimal("2000000"),
                anios_cotizados=Decimal("5"),
                anios_por_cotizar=Decimal("28"),
                smmlv=Decimal("1423500"),
            )
        )
        self.assertEqual(result["pension_invalidez"], Decimal("1161600.00"))
        self.assertEqual(result["pension_sobrevivencia"], Decimal("1214400.00"))
        self.assertEqual(result["pension_colpensiones"], Decimal("1408000.00"))
        self.assertEqual(result["brecha_fallecimiento"], Decimal("2785600.00"))
        self.assertEqual(result["capital_fallecimiento"], Decimal("557120000.00"))

# Create your tests here.
