from decimal import Decimal

from django.test import TestCase

from .services import calcular_brecha_proteccion


class SegurosRulesTests(TestCase):
    def test_gap_is_need_minus_existing_coverage(self):
        self.assertEqual(calcular_brecha_proteccion(Decimal("650000000"), Decimal("100000000")), Decimal("550000000"))

# Create your tests here.
