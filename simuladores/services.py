from decimal import Decimal

from clientes.services import record_timeline_event
from pensiones.services import ENGINE_VERSION, PensionInputs, RULESET_VERSION, calcular_panorama_ley_100, calcular_panorama_reforma

from .models import Simulacion


def run_excel_brechas_basico(*, cliente, consultor, inputs: dict, observaciones: str = "") -> Simulacion:
    escenario = inputs.get("escenario", "ley_100")
    pension_inputs = PensionInputs(
        ingreso_mensual=Decimal(str(inputs["ingreso_mensual"])),
        ibc_actual=Decimal(str(inputs["ibc_actual"])),
        ibc_ultimos_10_anios=Decimal(str(inputs["ibc_ultimos_10_anios"])),
        anios_cotizados=Decimal(str(inputs["anios_cotizados"])),
        anios_por_cotizar=Decimal(str(inputs["anios_por_cotizar"])),
        capital_actual_rais=Decimal(str(inputs.get("capital_actual_rais") or "0")),
        smmlv=Decimal(str(inputs.get("smmlv", "1423500"))),
    )
    if escenario == "reforma":
        resultados = calcular_panorama_reforma(pension_inputs)
        tipo = "brechas_panorama_reforma"
    else:
        resultados = calcular_panorama_ley_100(pension_inputs)
        tipo = "brechas_panorama_ley_100"
    sim = Simulacion.objects.create(
        cliente=cliente,
        consultor=consultor,
        tipo=tipo,
        version_motor=ENGINE_VERSION,
        normativa_version=resultados.get("ruleset_version", RULESET_VERSION),
        inputs_json={key: str(value) for key, value in inputs.items()},
        resultados_json={key: str(value) for key, value in resultados.items()},
        observaciones=observaciones,
    )
    record_timeline_event(cliente=cliente, actor=consultor, tipo="simulacion", titulo="Simulacion de brechas creada", descripcion=sim.tipo)
    return sim
