from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from .models import FondoPensiones


ENGINE_VERSION = "0.2.0"
RULESET_VERSION = "colombia-pensiones-2026-09-borrador"

FONDOS_PENSIONES_COLOMBIA_2026 = [
    {
        "nombre": "Colpensiones",
        "regimen": FondoPensiones.Regimen.RPM,
        "entidad": "Administradora Colombiana de Pensiones",
        "fuente": "https://www.colpensiones.gov.co/pensiones/publicaciones/120/que-es-el-rpm/",
        "observaciones": "Administradora estatal del Regimen de Prima Media.",
    },
    {
        "nombre": "Porvenir",
        "regimen": FondoPensiones.Regimen.RAIS,
        "entidad": "Sociedad Administradora de Fondos de Pensiones y Cesantias",
        "fuente": "https://www.superfinanciera.gov.co/publicaciones/38635/pensiones-cesantas-y-fiduciarias-38635/",
        "observaciones": "AFP privada vigilada por la Superintendencia Financiera.",
    },
    {
        "nombre": "Proteccion",
        "regimen": FondoPensiones.Regimen.RAIS,
        "entidad": "Administradora de Fondos de Pensiones y Cesantias Proteccion",
        "fuente": "https://www.superfinanciera.gov.co/publicaciones/38635/pensiones-cesantas-y-fiduciarias-38635/",
        "observaciones": "AFP privada vigilada por la Superintendencia Financiera.",
    },
    {
        "nombre": "Colfondos",
        "regimen": FondoPensiones.Regimen.RAIS,
        "entidad": "Colfondos S.A. Pensiones y Cesantias",
        "fuente": "https://www.superfinanciera.gov.co/publicaciones/38635/pensiones-cesantas-y-fiduciarias-38635/",
        "observaciones": "AFP privada vigilada por la Superintendencia Financiera.",
    },
    {
        "nombre": "Skandia Pensiones y Cesantias",
        "regimen": FondoPensiones.Regimen.RAIS,
        "entidad": "Skandia Pensiones y Cesantias S.A.",
        "fuente": "https://www.superfinanciera.gov.co/publicaciones/38635/pensiones-cesantas-y-fiduciarias-38635/",
        "observaciones": "AFP privada vigilada por la Superintendencia Financiera.",
    },
    {
        "nombre": "Positiva Compania de Seguros",
        "regimen": FondoPensiones.Regimen.ACCAI,
        "entidad": "Positiva Compania de Seguros S.A.",
        "fuente": "https://www.superfinanciera.gov.co/publicaciones/10115449/pensiones-ley-2381-de-2024/",
        "observaciones": "Autorizada por la SFC como ACCAI; no tratar como AFP tradicional ni activar reglas Ley 2381 sin revisar vigencia.",
    },
]


def ensure_default_pension_funds() -> None:
    for data in FONDOS_PENSIONES_COLOMBIA_2026:
        FondoPensiones.objects.get_or_create(nombre=data["nombre"], defaults=data)


@dataclass(frozen=True)
class PensionInputs:
    ingreso_mensual: Decimal
    ibc_actual: Decimal
    ibc_ultimos_10_anios: Decimal
    anios_cotizados: Decimal
    anios_por_cotizar: Decimal
    capital_actual_rais: Decimal = Decimal("0")
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


def calcular_panorama_reforma(inputs: PensionInputs) -> dict:
    minimo_neto = inputs.smmlv * Decimal("0.875")
    ibc_colpensiones = min(inputs.ibc_actual, inputs.smmlv * Decimal("2.3"))
    ibc_accai = max(inputs.ibc_actual - ibc_colpensiones, Decimal("0"))
    pension_invalidez = max(inputs.ibc_ultimos_10_anios * Decimal("0.66") * Decimal("0.88"), minimo_neto)
    pension_sobrevivencia = max(inputs.ibc_ultimos_10_anios * Decimal("0.69") * Decimal("0.88"), minimo_neto)
    pension_colpensiones = max(ibc_colpensiones * Decimal("0.71") * Decimal("0.88"), minimo_neto)
    capital_fedesarrollo = inputs.smmlv * Decimal("377")
    acumulacion_accai = ibc_accai * Decimal("0.115") * Decimal("12") * (inputs.anios_cotizados + inputs.anios_por_cotizar) + inputs.capital_actual_rais
    pension_accai = (Decimal("1.1") * inputs.smmlv * acumulacion_accai / capital_fedesarrollo) * Decimal("0.88") if capital_fedesarrollo else Decimal("0")
    pension_total = pension_colpensiones + pension_accai
    return {
        "engine_version": ENGINE_VERSION,
        "ruleset_version": f"{RULESET_VERSION}-reforma-no-vigencia-plena",
        "estado_normativo": "Modelo consultivo no activado como regla juridica vigente plena",
        "ibc_colpensiones": money(ibc_colpensiones),
        "ibc_accai": money(ibc_accai),
        "pension_invalidez": money(pension_invalidez),
        "pension_sobrevivencia": money(pension_sobrevivencia),
        "pension_colpensiones": money(pension_colpensiones),
        "pension_accai": money(pension_accai),
        "pension_total_sistema": money(pension_total),
        "brecha_fallecimiento": money(inputs.ingreso_mensual - pension_sobrevivencia),
        "brecha_invalidez": money(inputs.ingreso_mensual - pension_invalidez),
        "brecha_vejez_sistema": money(inputs.ingreso_mensual - pension_total),
        "capital_fallecimiento": money((inputs.ingreso_mensual - pension_sobrevivencia) * Decimal("200")),
        "capital_invalidez": money((inputs.ingreso_mensual - pension_invalidez) * Decimal("200")),
        "capital_vejez_sistema": money((inputs.ingreso_mensual - pension_total) * Decimal("200")),
    }
