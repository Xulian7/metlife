from decimal import Decimal

from django.test import TestCase

from .models import FondoPensiones
from .services import PensionInputs, calcular_comparativo_pensional, calcular_panorama_ley_100, calcular_panorama_reforma, ensure_default_pension_funds


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

    def test_default_pension_funds_include_regimes(self):
        ensure_default_pension_funds()
        self.assertEqual(FondoPensiones.objects.get(nombre="Colpensiones").regimen, FondoPensiones.Regimen.RPM)
        self.assertEqual(FondoPensiones.objects.get(nombre="Porvenir").regimen, FondoPensiones.Regimen.RAIS)

    def test_reforma_calculates_pillar_split(self):
        result = calcular_panorama_reforma(
            PensionInputs(
                ingreso_mensual=Decimal("4000000"),
                ibc_actual=Decimal("5000000"),
                ibc_ultimos_10_anios=Decimal("4000000"),
                anios_cotizados=Decimal("10"),
                anios_por_cotizar=Decimal("20"),
                smmlv=Decimal("1423500"),
            )
        )
        self.assertEqual(result["ibc_colpensiones"], Decimal("3274050.00"))
        self.assertEqual(result["ibc_accai"], Decimal("1725950.00"))
        self.assertIn("estado_normativo", result)

    def test_comparative_projection_includes_legal_milestones(self):
        result = calcular_comparativo_pensional(
            PensionInputs(
                ingreso_mensual=Decimal("4000000"),
                ibc_actual=Decimal("3000000"),
                ibc_ultimos_10_anios=Decimal("2800000"),
                anios_cotizados=Decimal("12"),
                anios_por_cotizar=Decimal("18"),
                meses_cotizados_anio=Decimal("9"),
                smmlv=Decimal("1423500"),
                sexo="femenino",
            )
        )
        self.assertEqual(result["contexto"]["edad_requisito_rpm"], Decimal("57"))
        self.assertEqual(result["contexto"]["semanas_actuales"], Decimal("624.00"))
        self.assertEqual(len(result["proyecciones"]), 4)
        self.assertIn("fuentes", result)

# Create your tests here.
