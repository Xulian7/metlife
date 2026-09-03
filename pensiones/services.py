from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


ENGINE_VERSION = "0.1.0"
RULESET_VERSION = "colombia-pensiones-2026-09-borrador"


@dataclass(frozen=True)
class PensionInputs:
    ingreso_mensual: Decimal
    ibc_actual: Decimal
    ibc_ultimos_10_anios: Decimal
    anios_cotizados: Decimal
    anios_por_cotizar: Decimal
    smmlv: Decimal = Decimal("1423500")


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calcular_panorama_ley_100(inputs: PensionInputs) -> dict:
    minimo_neto = inputs.smmlv * Decimal("0.88")
    invalidez_base = inputs.ibc_ultimos_10_anios * Decimal("0.66")
    sobrevivencia_base = inputs.ibc_ultimos_10_anios * Decimal("0.69")
    pension_invalidez = invalidez_base * Decimal("0.88") if invalidez_base > minimo_neto else minimo_neto
    pension_sobrevivencia = sobrevivencia_base * Decimal("0.88") if sobrevivencia_base > minimo_neto else minimo_neto
    pension_colpensiones_base = inputs.ibc_actual * Decimal("0.80") * Decimal("0.875")
    pension_colpensiones = inputs.ibc_actual * Decimal("0.80") * Decimal("0.88") if pension_colpensiones_base > minimo_neto else minimo_neto
    capital_fedesarrollo = inputs.smmlv * Decimal("377")
    acumulacion = inputs.ibc_actual * Decimal("0.115") * Decimal("12") * (inputs.anios_cotizados + inputs.anios_por_cotizar)
    pension_privada_bruta = inputs.smmlv * (acumulacion / capital_fedesarrollo) * Decimal("0.88")
    pension_privada = max(pension_privada_bruta, minimo_neto)
    return {
        "engine_version": ENGINE_VERSION,
        "ruleset_version": RULESET_VERSION,
        "pension_invalidez": money(pension_invalidez),
        "pension_sobrevivencia": money(pension_sobrevivencia),
        "pension_colpensiones": money(pension_colpensiones),
        "pension_privada": money(pension_privada),
        "brecha_fallecimiento": money(inputs.ingreso_mensual - pension_sobrevivencia),
        "brecha_invalidez": money(inputs.ingreso_mensual - pension_invalidez),
        "brecha_vejez_colpensiones": money(inputs.ingreso_mensual - pension_colpensiones),
        "brecha_vejez_privada": money(inputs.ingreso_mensual - pension_privada),
        "capital_fallecimiento": money((inputs.ingreso_mensual - pension_sobrevivencia) * Decimal("200")),
        "capital_invalidez": money((inputs.ingreso_mensual - pension_invalidez) * Decimal("200")),
        "capital_vejez_colpensiones": money((inputs.ingreso_mensual - pension_colpensiones) * Decimal("200")),
        "capital_vejez_privada": money((inputs.ingreso_mensual - pension_privada) * Decimal("200")),
    }
