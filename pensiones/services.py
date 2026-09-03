from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from .models import FondoPensiones


ENGINE_VERSION = "0.4.0"
RULESET_VERSION = "colombia-pensiones-2026-09-borrador"
WEEKS_PER_YEAR = Decimal("52")
RPM_REQUIRED_WEEKS = Decimal("1300")
RAIS_MINIMUM_GUARANTEE_WEEKS = Decimal("1150")
TRANSITION_WEEKS_WOMEN = Decimal("750")
TRANSITION_WEEKS_MEN = Decimal("900")
TRANSITION_CUTOFF_DATE = date(2025, 6, 30)

PENSION_GLOSSARY = [
    {
        "termino": "RPM",
        "nombre": "Régimen de Prima Media",
        "definicion": "Régimen público administrado por Colpensiones. La pensión depende de edad, semanas cotizadas y reglas de liquidación aplicables, no de una cuenta individual del afiliado.",
    },
    {
        "termino": "RAIS",
        "nombre": "Régimen de Ahorro Individual con Solidaridad",
        "definicion": "Régimen administrado por fondos privados. La prestación depende principalmente del capital acumulado, rendimientos, bono pensional si aplica y modalidad de pensión.",
    },
    {
        "termino": "ACCAI",
        "nombre": "Administradora del Componente Complementario de Ahorro Individual",
        "definicion": "Figura asociada al sistema de pilares de la Ley 2381. En esta plataforma se muestra como escenario consultivo mientras se valida su aplicación jurídica plena.",
    },
    {
        "termino": "IBC",
        "nombre": "Ingreso Base de Cotización",
        "definicion": "Valor sobre el cual se calculan los aportes a seguridad social. No siempre coincide con el ingreso total ni con el salario recibido.",
    },
    {
        "termino": "IBL",
        "nombre": "Ingreso Base de Liquidación",
        "definicion": "Promedio usado para liquidar una prestación pensional según la regla aplicable. Requiere historia laboral y parámetros de actualización cuando corresponda.",
    },
    {
        "termino": "SMMLV",
        "nombre": "Salario Mínimo Mensual Legal Vigente",
        "definicion": "Parámetro legal usado como referencia para mesada mínima, topes y cálculos comparativos. Debe mantenerse versionado por año.",
    },
    {
        "termino": "Semanas cotizadas",
        "nombre": "Tiempo reconocido de cotización",
        "definicion": "Unidad usada para verificar requisitos pensionales. En proyecciones simples se estima desde años cotizados, pero una historia laboral real debe validar periodos y novedades.",
    },
    {
        "termino": "Régimen de transición",
        "nombre": "Conservación de reglas anteriores",
        "definicion": "Condición que permite conservar reglas de Ley 100/Ley 797 frente a la Ley 2381 si se cumplen semanas mínimas al corte legal: 750 para mujeres y 900 para hombres.",
    },
    {
        "termino": "Pensión de invalidez",
        "nombre": "Prestación por pérdida de capacidad laboral",
        "definicion": "Estimación de ingreso pensional ante invalidez. El reconocimiento real depende de origen, porcentaje de pérdida, semanas, fecha de estructuración y entidad competente.",
    },
    {
        "termino": "Pensión de sobrevivencia",
        "nombre": "Prestación para beneficiarios",
        "definicion": "Estimación del ingreso que podrían recibir beneficiarios ante fallecimiento del afiliado o pensionado, sujeto a requisitos y beneficiarios acreditados.",
    },
    {
        "termino": "Brecha de invalidez",
        "nombre": "Diferencia ante invalidez",
        "definicion": "Diferencia entre el ingreso mensual objetivo del cliente y la pensión estimada por invalidez. Ayuda a dimensionar necesidad de protección complementaria.",
    },
    {
        "termino": "Brecha de fallecimiento",
        "nombre": "Diferencia ante fallecimiento",
        "definicion": "Diferencia entre el ingreso mensual objetivo del hogar y la pensión estimada de sobrevivencia. Sirve para estimar necesidad de capital o cobertura.",
    },
    {
        "termino": "Brecha de vejez",
        "nombre": "Diferencia en retiro",
        "definicion": "Diferencia entre el ingreso mensual objetivo y la pensión estimada de vejez en cada panorama. Permite comparar escenarios de retiro.",
    },
    {
        "termino": "Capital Fedesarrollo",
        "nombre": "Referencia de capital para estimación",
        "definicion": "Factor usado por el simulador como referencia funcional para convertir capital proyectado en una mesada estimada. Es un supuesto de simulación, no una liquidación oficial.",
    },
    {
        "termino": "Capital de brecha",
        "nombre": "Capital necesario estimado",
        "definicion": "Resultado de multiplicar una brecha mensual por un factor de capital. Sirve como aproximación comercial y financiera de protección, no como obligación legal.",
    },
    {
        "termino": "Densidad de cotización",
        "nombre": "Meses cotizados por año",
        "definicion": "Supuesto que indica cuántos meses al año seguirá cotizando la persona. La simulación muestra impactos para 12, 9, 6 y 0 meses.",
    },
]

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
    fecha_nacimiento: date | None = None
    sexo: str = ""
    edad_actual: Decimal | None = None
    meses_cotizados_anio: Decimal = Decimal("12")
    tasa_renta_mensual: Decimal = Decimal("0.005")
    factor_capital_brecha: Decimal = Decimal("200")
    factor_capital_fedesarrollo: Decimal = Decimal("377")
    tasa_aporte_acumulacion: Decimal = Decimal("0.115")
    tasa_descuento_neto_ley_100: Decimal = Decimal("0.88")
    tasa_descuento_neto_reforma: Decimal = Decimal("0.875")


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def number(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_age(born: date | None, today: date | None = None) -> Decimal | None:
    if not born:
        return None
    today = today or date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return Decimal(age)


def normalizar_sexo(sexo: str) -> str:
    value = (sexo or "").strip().lower()
    if value in {"f", "femenino", "mujer"}:
        return "mujer"
    if value in {"m", "masculino", "hombre"}:
        return "hombre"
    return "no_informado"


def edad_pension_referencia(sexo: str) -> Decimal:
    return Decimal("57") if normalizar_sexo(sexo) == "mujer" else Decimal("62")


def semanas_transicion_requeridas(sexo: str) -> Decimal:
    return TRANSITION_WEEKS_WOMEN if normalizar_sexo(sexo) == "mujer" else TRANSITION_WEEKS_MEN


def weeks_from_years(years: Decimal) -> Decimal:
    return years * WEEKS_PER_YEAR


def years_until_weeks(current_weeks: Decimal, target_weeks: Decimal, months_per_year: Decimal) -> Decimal | None:
    annual_weeks = WEEKS_PER_YEAR * (months_per_year / Decimal("12"))
    if current_weeks >= target_weeks:
        return Decimal("0")
    if annual_weeks <= 0:
        return None
    return (target_weeks - current_weeks) / annual_weeks


def pension_context(inputs: PensionInputs) -> dict:
    edad = inputs.edad_actual if inputs.edad_actual is not None else calculate_age(inputs.fecha_nacimiento)
    edad_ref = edad_pension_referencia(inputs.sexo)
    semanas_actuales = weeks_from_years(inputs.anios_cotizados)
    semanas_transicion = semanas_transicion_requeridas(inputs.sexo)
    cumple_transicion = semanas_actuales >= semanas_transicion
    semanas_futuras = weeks_from_years(inputs.anios_por_cotizar) * (inputs.meses_cotizados_anio / Decimal("12"))
    semanas_proyectadas = semanas_actuales + semanas_futuras
    years_to_1300 = years_until_weeks(semanas_actuales, RPM_REQUIRED_WEEKS, inputs.meses_cotizados_anio)
    edad_cumple_semanas = None if edad is None or years_to_1300 is None else edad + years_to_1300
    edad_estimada_rpm = edad_ref
    if edad_cumple_semanas is not None and edad_cumple_semanas > edad_ref:
        edad_estimada_rpm = edad_cumple_semanas
    return {
        "sexo_normalizado": normalizar_sexo(inputs.sexo),
        "edad_actual": number(edad) if edad is not None else None,
        "edad_requisito_rpm": edad_ref,
        "semanas_actuales": number(semanas_actuales),
        "fecha_corte_transicion": TRANSITION_CUTOFF_DATE.isoformat(),
        "semanas_requeridas_transicion_ley_2381": number(semanas_transicion),
        "cumple_regimen_transicion_ley_2381": cumple_transicion,
        "regimen_simulacion_recomendado": "Ley 100 / Ley 797" if cumple_transicion else "Reforma pensional consultiva",
        "fundamento_decision_regimen": (
            "Cumple semanas de transicion: conserva reglas Ley 100 segun articulo 75 Ley 2381."
            if cumple_transicion
            else "No alcanza semanas de transicion; se muestra Reforma como escenario consultivo sujeto a estado juridico."
        ),
        "semanas_proyectadas": number(semanas_proyectadas),
        "semanas_faltantes_rpm": number(max(RPM_REQUIRED_WEEKS - semanas_actuales, Decimal("0"))),
        "semanas_faltantes_rais_garantia": number(max(RAIS_MINIMUM_GUARANTEE_WEEKS - semanas_actuales, Decimal("0"))),
        "edad_estimada_cumplimiento_semanas": number(edad_cumple_semanas) if edad_cumple_semanas is not None else None,
        "edad_estimada_pension_rpm": number(edad_estimada_rpm) if edad is not None else None,
        "cumple_semanas_rpm_proyectadas": semanas_proyectadas >= RPM_REQUIRED_WEEKS,
        "cumple_garantia_minima_rais_proyectada": semanas_proyectadas >= RAIS_MINIMUM_GUARANTEE_WEEKS,
    }


def calcular_panorama_automatico(inputs: PensionInputs) -> dict:
    contexto = pension_context(inputs)
    if contexto["cumple_regimen_transicion_ley_2381"]:
        result = calcular_panorama_ley_100(inputs)
        result["tipo_decision"] = "automatico_por_semanas"
        result["regimen_aplicado"] = "Ley 100 / Ley 797"
        result["fundamento_decision_regimen"] = contexto["fundamento_decision_regimen"]
        result["fuentes"] = OFFICIAL_SOURCES
        return result
    result = calcular_panorama_reforma(inputs)
    result["tipo_decision"] = "automatico_por_semanas"
    result["regimen_aplicado"] = "Reforma pensional consultiva"
    result["fundamento_decision_regimen"] = contexto["fundamento_decision_regimen"]
    result["fuentes"] = OFFICIAL_SOURCES
    return result


def calcular_panorama_ley_100(inputs: PensionInputs) -> dict:
    minimo_neto = inputs.smmlv * inputs.tasa_descuento_neto_ley_100
    invalidez_base = inputs.ibc_ultimos_10_anios * Decimal("0.66")
    sobrevivencia_base = inputs.ibc_ultimos_10_anios * Decimal("0.69")
    pension_invalidez = invalidez_base * inputs.tasa_descuento_neto_ley_100 if invalidez_base > minimo_neto else minimo_neto
    pension_sobrevivencia = sobrevivencia_base * inputs.tasa_descuento_neto_ley_100 if sobrevivencia_base > minimo_neto else minimo_neto
    pension_colpensiones_base = inputs.ibc_actual * Decimal("0.80") * Decimal("0.875")
    pension_colpensiones = inputs.ibc_actual * Decimal("0.80") * inputs.tasa_descuento_neto_ley_100 if pension_colpensiones_base > minimo_neto else minimo_neto
    capital_fedesarrollo = inputs.smmlv * inputs.factor_capital_fedesarrollo
    acumulacion = inputs.ibc_actual * inputs.tasa_aporte_acumulacion * Decimal("12") * (inputs.anios_cotizados + inputs.anios_por_cotizar) + inputs.capital_actual_rais
    pension_privada_bruta = inputs.smmlv * (acumulacion / capital_fedesarrollo) * inputs.tasa_descuento_neto_ley_100
    pension_privada = max(pension_privada_bruta, minimo_neto)
    contexto = pension_context(inputs)
    return {
        "engine_version": ENGINE_VERSION,
        "ruleset_version": RULESET_VERSION,
        "contexto": contexto,
        "minimo_neto": money(minimo_neto),
        "capital_fedesarrollo": money(capital_fedesarrollo),
        "acumulacion_proyectada_rais": money(acumulacion),
        "pension_invalidez": money(pension_invalidez),
        "pension_sobrevivencia": money(pension_sobrevivencia),
        "pension_colpensiones": money(pension_colpensiones),
        "pension_privada": money(pension_privada),
        "brecha_fallecimiento": money(inputs.ingreso_mensual - pension_sobrevivencia),
        "brecha_invalidez": money(inputs.ingreso_mensual - pension_invalidez),
        "brecha_vejez_colpensiones": money(inputs.ingreso_mensual - pension_colpensiones),
        "brecha_vejez_privada": money(inputs.ingreso_mensual - pension_privada),
        "capital_fallecimiento": money((inputs.ingreso_mensual - pension_sobrevivencia) * inputs.factor_capital_brecha),
        "capital_invalidez": money((inputs.ingreso_mensual - pension_invalidez) * inputs.factor_capital_brecha),
        "capital_vejez_colpensiones": money((inputs.ingreso_mensual - pension_colpensiones) * inputs.factor_capital_brecha),
        "capital_vejez_privada": money((inputs.ingreso_mensual - pension_privada) * inputs.factor_capital_brecha),
    }


def calcular_panorama_reforma(inputs: PensionInputs) -> dict:
    minimo_neto = inputs.smmlv * inputs.tasa_descuento_neto_reforma
    ibc_colpensiones = min(inputs.ibc_actual, inputs.smmlv * Decimal("2.3"))
    ibc_accai = max(inputs.ibc_actual - ibc_colpensiones, Decimal("0"))
    pension_invalidez = max(inputs.ibc_ultimos_10_anios * Decimal("0.66") * Decimal("0.88"), minimo_neto)
    pension_sobrevivencia = max(inputs.ibc_ultimos_10_anios * Decimal("0.69") * Decimal("0.88"), minimo_neto)
    pension_colpensiones = max(ibc_colpensiones * Decimal("0.71") * Decimal("0.88"), minimo_neto)
    capital_fedesarrollo = inputs.smmlv * inputs.factor_capital_fedesarrollo
    acumulacion_accai = ibc_accai * inputs.tasa_aporte_acumulacion * Decimal("12") * (inputs.anios_cotizados + inputs.anios_por_cotizar) + inputs.capital_actual_rais
    pension_accai = (Decimal("1.1") * inputs.smmlv * acumulacion_accai / capital_fedesarrollo) * inputs.tasa_descuento_neto_ley_100 if capital_fedesarrollo else Decimal("0")
    pension_total = pension_colpensiones + pension_accai
    contexto = pension_context(inputs)
    return {
        "engine_version": ENGINE_VERSION,
        "ruleset_version": f"{RULESET_VERSION}-reforma-no-vigencia-plena",
        "estado_normativo": "Modelo consultivo no activado como regla jurídica vigente plena",
        "contexto": contexto,
        "minimo_neto": money(minimo_neto),
        "capital_fedesarrollo": money(capital_fedesarrollo),
        "ibc_colpensiones": money(ibc_colpensiones),
        "ibc_accai": money(ibc_accai),
        "acumulacion_proyectada_accai": money(acumulacion_accai),
        "pension_invalidez": money(pension_invalidez),
        "pension_sobrevivencia": money(pension_sobrevivencia),
        "pension_colpensiones": money(pension_colpensiones),
        "pension_accai": money(pension_accai),
        "pension_total_sistema": money(pension_total),
        "brecha_fallecimiento": money(inputs.ingreso_mensual - pension_sobrevivencia),
        "brecha_invalidez": money(inputs.ingreso_mensual - pension_invalidez),
        "brecha_vejez_sistema": money(inputs.ingreso_mensual - pension_total),
        "capital_fallecimiento": money((inputs.ingreso_mensual - pension_sobrevivencia) * inputs.factor_capital_brecha),
        "capital_invalidez": money((inputs.ingreso_mensual - pension_invalidez) * inputs.factor_capital_brecha),
        "capital_vejez_sistema": money((inputs.ingreso_mensual - pension_total) * inputs.factor_capital_brecha),
    }


def calcular_comparativo_pensional(inputs: PensionInputs) -> dict:
    ley_100 = calcular_panorama_ley_100(inputs)
    reforma = calcular_panorama_reforma(inputs)
    contexto = pension_context(inputs)
    return {
        "engine_version": ENGINE_VERSION,
        "ruleset_version": f"{RULESET_VERSION}-comparativo",
        "contexto": contexto,
        "resumen": {
            "ingreso_mensual": money(inputs.ingreso_mensual),
            "ibc_actual": money(inputs.ibc_actual),
            "ibc_ultimos_10_anios": money(inputs.ibc_ultimos_10_anios),
            "smmlv": money(inputs.smmlv),
            "edad_actual": contexto["edad_actual"],
            "edad_requisito_rpm": contexto["edad_requisito_rpm"],
            "semanas_actuales": contexto["semanas_actuales"],
            "semanas_requeridas_transicion_ley_2381": contexto["semanas_requeridas_transicion_ley_2381"],
            "cumple_regimen_transicion_ley_2381": contexto["cumple_regimen_transicion_ley_2381"],
            "regimen_simulacion_recomendado": contexto["regimen_simulacion_recomendado"],
            "semanas_proyectadas": contexto["semanas_proyectadas"],
            "fondo_actual": "",
        },
        "ley_100": ley_100,
        "reforma": reforma,
        "comparacion": {
            "pension_vejez_rpm_ley_100": ley_100["pension_colpensiones"],
            "pension_vejez_rais_ley_100": ley_100["pension_privada"],
            "pension_total_reforma": reforma["pension_total_sistema"],
            "brecha_menor_vejez": min(
                ley_100["brecha_vejez_colpensiones"],
                ley_100["brecha_vejez_privada"],
                reforma["brecha_vejez_sistema"],
            ),
        },
        "proyecciones": build_projection_rows(inputs),
        "alertas": build_alerts(inputs, contexto),
        "fuentes": OFFICIAL_SOURCES,
    }


def build_projection_rows(inputs: PensionInputs) -> list[dict]:
    rows = []
    for months in [Decimal("12"), Decimal("9"), Decimal("6"), Decimal("0")]:
        projected = PensionInputs(**{**inputs.__dict__, "meses_cotizados_anio": months})
        contexto = pension_context(projected)
        ley_100 = calcular_panorama_ley_100(projected)
        rows.append(
            {
                "cotiza_meses_anio": number(months),
                "semanas_proyectadas": contexto["semanas_proyectadas"],
                "edad_estimada_pension_rpm": contexto["edad_estimada_pension_rpm"],
                "cumple_rpm": contexto["cumple_semanas_rpm_proyectadas"],
                "cumple_garantia_rais": contexto["cumple_garantia_minima_rais_proyectada"],
                "pension_rpm_estimada": ley_100["pension_colpensiones"],
                "pension_rais_estimada": ley_100["pension_privada"],
            }
        )
    return rows


def build_alerts(inputs: PensionInputs, contexto: dict) -> list[str]:
    alerts = []
    if contexto["sexo_normalizado"] == "no_informado":
        alerts.append("Sexo no informado: se usa edad de referencia conservadora de 62 años. Completar este dato mejora la proyección.")
    if contexto["cumple_regimen_transicion_ley_2381"]:
        alerts.append("Cumple umbral de transición Ley 2381: se debe conservar simulación bajo Ley 100 / Ley 797, validando semanas al 30 de junio de 2025.")
    else:
        alerts.append("No cumple umbral de transición Ley 2381 con las semanas informadas; la Reforma se muestra como escenario consultivo por estado jurídico.")
    if not contexto["cumple_semanas_rpm_proyectadas"]:
        alerts.append("Con la densidad de cotización indicada no se proyectan 1.300 semanas para RPM; revisar alternativas o continuidad de aportes.")
    if not contexto["cumple_garantia_minima_rais_proyectada"]:
        alerts.append("No se proyectan 1.150 semanas para garantia de pension minima RAIS; esta alerta no reemplaza estudio de capital individual.")
    if inputs.ibc_actual < inputs.smmlv:
        alerts.append("IBC actual inferior al SMMLV parametrizado; validar dato antes de usar resultados en asesoria.")
    alerts.append("La hoja Reforma es un escenario consultivo: Ley 2381 de 2024 no se activa como vigencia plena por defecto.")
    return alerts


OFFICIAL_SOURCES = [
    {
        "nombre": "Colpensiones - requisitos RPM",
        "url": "https://www.colpensiones.gov.co/publicaciones/3650/preguntas-frecuentes/",
        "nota": "Edad 57 mujeres, 62 hombres y 1.300 semanas para pension de vejez en RPM.",
    },
    {
        "nombre": "Colpensiones - funcionamiento sistema pensional",
        "url": "https://www.colpensiones.gov.co/publicaciones/2841/como-funciona-el-sistema-pensional-colombiano/",
        "nota": "Alternativas Colpensiones y fondos privados.",
    },
    {
        "nombre": "Superfinanciera Circular 12 de 2024",
        "url": "https://normativa.colpensiones.gov.co/colpens/compilacion/docs/circular_superfinanciera_0012_2024.htm",
        "nota": "Proyecciones de asesoría por densidad de cotización: 12, 9, 6 o 0 meses al año.",
    },
    {
        "nombre": "Corte Constitucional Auto 841 de 2025",
        "url": "https://www.corteconstitucional.gov.co/relatoria/autos/2025/a841-25.htm",
        "nota": "Suspension de entrada en vigencia general de Ley 2381 de 2024.",
    },
    {
        "nombre": "Corte Constitucional C-327 de 2025",
        "url": "https://www.corteconstitucional.gov.co/relatoria/2025/C-327-25.htm",
        "nota": "Reitera suspension con excepciones de Ley 2381 de 2024.",
    },
    {
        "nombre": "Ley 2381 de 2024 - régimen de transición",
        "url": "https://normativa.colpensiones.gov.co/compilacion/docs/ley_2381_2024.htm",
        "nota": "Articulo 75: 750 semanas mujeres y 900 semanas hombres para conservar Ley 100.",
    },
    {
        "nombre": "Corte Constitucional C-054 de 2024",
        "url": "https://normativa.colpensiones.gov.co/colpens/compilacion/docs/c-054_2024.htm",
        "nota": "Garantia de pension minima RAIS: edad, 1.150 semanas e insuficiencia de capital.",
    },
]
