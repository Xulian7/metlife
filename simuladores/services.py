from decimal import Decimal

from clientes.services import record_timeline_event
from pensiones.services import (
    ENGINE_VERSION,
    PensionInputs,
    RULESET_VERSION,
    calcular_comparativo_pensional,
    calcular_panorama_ley_100,
    calcular_panorama_reforma,
)

from .models import Simulacion


def to_decimal(value, default: str = "0") -> Decimal:
    if value in (None, ""):
        value = default
    return Decimal(str(value))


def to_jsonable(value):
    if isinstance(value, Decimal):
        return str(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    return value


def run_excel_brechas_basico(*, cliente, consultor, inputs: dict, observaciones: str = "") -> Simulacion:
    escenario = inputs.get("escenario", "comparativo")
    pension_inputs = PensionInputs(
        ingreso_mensual=to_decimal(inputs["ingreso_mensual"]),
        ibc_actual=to_decimal(inputs["ibc_actual"]),
        ibc_ultimos_10_anios=to_decimal(inputs["ibc_ultimos_10_anios"]),
        anios_cotizados=to_decimal(inputs["anios_cotizados"]),
        anios_por_cotizar=to_decimal(inputs["anios_por_cotizar"]),
        capital_actual_rais=to_decimal(inputs.get("capital_actual_rais")),
        smmlv=to_decimal(inputs.get("smmlv"), "1423500"),
        fecha_nacimiento=inputs.get("fecha_nacimiento") or cliente.fecha_nacimiento,
        sexo=inputs.get("sexo") or cliente.sexo,
        edad_actual=to_decimal(inputs.get("edad_actual")) if inputs.get("edad_actual") not in (None, "") else None,
        meses_cotizados_anio=to_decimal(inputs.get("meses_cotizados_anio"), "12"),
        tasa_renta_mensual=to_decimal(inputs.get("tasa_renta_mensual"), "0.005"),
        factor_capital_brecha=to_decimal(inputs.get("factor_capital_brecha"), "200"),
        factor_capital_fedesarrollo=to_decimal(inputs.get("factor_capital_fedesarrollo"), "377"),
        tasa_aporte_acumulacion=to_decimal(inputs.get("tasa_aporte_acumulacion"), "0.115"),
    )
    if escenario == "ley_100":
        resultados = calcular_panorama_ley_100(pension_inputs)
        tipo = "brechas_panorama_ley_100"
    elif escenario == "reforma":
        resultados = calcular_panorama_reforma(pension_inputs)
        tipo = "brechas_panorama_reforma"
    else:
        resultados = calcular_comparativo_pensional(pension_inputs)
        tipo = "brechas_pensional_comparativo"
    if isinstance(resultados.get("resumen"), dict):
        resultados["resumen"]["fondo_actual"] = str(cliente.fondo_pensiones or "Sin fondo seleccionado")
        resultados["resumen"]["regimen_actual"] = cliente.regimen_pensional
    sim = Simulacion.objects.create(
        cliente=cliente,
        consultor=consultor,
        tipo=tipo,
        version_motor=ENGINE_VERSION,
        normativa_version=resultados.get("ruleset_version", RULESET_VERSION),
        inputs_json=to_jsonable(inputs),
        resultados_json=to_jsonable(resultados),
        observaciones=observaciones,
    )
    record_timeline_event(cliente=cliente, actor=consultor, tipo="simulacion", titulo="Simulacion de brechas creada", descripcion=sim.tipo)
    return sim
