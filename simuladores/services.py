from decimal import Decimal

from clientes.services import record_timeline_event
from pensiones.services import ENGINE_VERSION, PensionInputs, RULESET_VERSION, calcular_panorama_ley_100

from .models import Simulacion


def run_excel_brechas_basico(*, cliente, consultor, inputs: dict, observaciones: str = "") -> Simulacion:
    pension_inputs = PensionInputs(
        ingreso_mensual=Decimal(str(inputs["ingreso_mensual"])),
        ibc_actual=Decimal(str(inputs["ibc_actual"])),
        ibc_ultimos_10_anios=Decimal(str(inputs["ibc_ultimos_10_anios"])),
        anios_cotizados=Decimal(str(inputs["anios_cotizados"])),
        anios_por_cotizar=Decimal(str(inputs["anios_por_cotizar"])),
        smmlv=Decimal(str(inputs.get("smmlv", "1423500"))),
    )
    resultados = calcular_panorama_ley_100(pension_inputs)
    sim = Simulacion.objects.create(
        cliente=cliente,
        consultor=consultor,
        tipo="brechas_ley_100_basico",
        version_motor=ENGINE_VERSION,
        normativa_version=RULESET_VERSION,
        inputs_json={key: str(value) for key, value in inputs.items()},
        resultados_json={key: str(value) for key, value in resultados.items()},
        observaciones=observaciones,
    )
    record_timeline_event(cliente=cliente, actor=consultor, tipo="simulacion", titulo="Simulacion de brechas creada", descripcion=sim.tipo)
    return sim
