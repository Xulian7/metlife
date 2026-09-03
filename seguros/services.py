from decimal import Decimal


def calcular_brecha_proteccion(necesidad_total: Decimal, cobertura_existente: Decimal) -> Decimal:
    return necesidad_total - cobertura_existente
