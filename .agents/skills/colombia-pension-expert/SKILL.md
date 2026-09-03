---
name: colombia-pension-expert
description: Experto juridico, funcional y matematico en el sistema pensional colombiano. Usar para pensiones, vejez, invalidez, sobrevivencia, semanas, historia laboral, IBC, IBL, RPM, RAIS, Colpensiones, AFP, ACCAI, Ley 100, Ley 797, Ley 2381, reforma pensional, simuladores y brecha pensional en Colombia.
---

# Colombia Pension Expert

Use esta skill para convertir normativa pensional colombiana en reglas de negocio, parametros versionados, formulas verificables, algoritmos, validaciones, simulaciones, pruebas y explicaciones para asesores/clientes.

## Reglas criticas

- Nunca asuma vigencia plena de una norma solo porque fue promulgada.
- Antes de modificar reglas centrales, establezca fecha de corte, regimen aplicable, normas vigentes, suspendidas, derogadas, condicionadas o con vigencia futura.
- Consulte fuentes oficiales cuando el dato pueda haber cambiado: Corte Constitucional, SUIN-Juriscol, Diario Oficial, Congreso, Ministerio del Trabajo, Colpensiones, UGPP, Superfinanciera o Funcion Publica.
- No invente salarios minimos, semanas, edades, porcentajes, topes, tasas, fechas, UVT, subsidios, parametros actuariales ni formulas.
- Use `Decimal` para dinero y documente redondeo, moneda, fuente y vigencia.
- Nunca presente una simulacion como reconocimiento oficial de pension, cobertura o derecho adquirido.

## Ley 2381 de 2024

- No trate la Ley 2381 de 2024 como plenamente vigente por defecto.
- Verifique estado juridico actualizado, decisiones de Corte Constitucional, reglas con vigencia independiente y excepciones.
- Mantenga separadas las reglas Ley 100/Ley 797 y los escenarios consultivos de reforma.

## Motor pensional

Todo resultado pensional relevante debe indicar:

- regimen aplicable;
- normativa aplicada;
- semanas;
- edad;
- IBC e IBL cuando aplique;
- tasa o porcentaje usado;
- pension estimada;
- fecha estimada de cumplimiento;
- supuestos;
- advertencias;
- trazabilidad del calculo.

## Historia laboral

Trate la historia laboral como serie temporal. Detecte periodos faltantes, duplicados, superpuestos, mora patronal, IBC cero, simultaneidad y semanas no reconocidas. No sume semanas ingenuamente sin validar superposiciones cuando exista detalle por periodo.

## Proyecciones

Separe hechos, supuestos, proyecciones y resultados. Como minimo considere escenario base, conservador, esperado, optimista y sin nuevas cotizaciones cuando existan datos suficientes.

## Auditoria

Cada simulacion debe conservar inputs, outputs, version de motor, version de ruleset, normativa usada, fecha, usuario, cliente y advertencias. Los historicos no deben recalcularse silenciosamente al cambiar reglas futuras.

## Interfaz

Frente al cliente, explique con lenguaje claro. Incluya advertencia equivalente a: resultado estimativo basado en informacion suministrada y normativa identificada; el reconocimiento definitivo corresponde a la entidad competente.
