---
name: pensiones-seguros-colombia
description: Analizar casos de pensiones, proteccion para la vejez y seguros en Colombia con control de vigencias, fuentes oficiales y simulaciones auditables.
---

# Pensiones y Seguros Colombia

Use esta skill para trabajar en reglas, diagnosticos o simulaciones de pensiones, proteccion para la vejez, seguridad social y seguros en Colombia dentro de este repositorio.

## Reglas criticas

- Ningun calculo juridico/pensional puede modificar su logica basandose unicamente en conocimiento memorizado del modelo cuando el dato pueda haber cambiado. Debe comprobarse contra las fuentes normativas correspondientes.
- No presente una simulacion como reconocimiento oficial de pension, cobertura o derecho adquirido.
- Diferencie dato capturado, calculo, alerta, oportunidad comercial, recomendacion y concepto juridico.
- Use `Decimal` para dinero y documente redondeo, moneda, fuente y vigencia.

## Flujo recomendado

1. Revise el caso: edad, sexo cuando aplique, semanas, IBC, historia laboral, regimen, beneficiarios, capital, dependientes y objetivos.
2. Verifique normativa vigente o aplicable segun `fecha_simulacion`.
3. Clasifique cada norma como vigente, suspendida, vigente parcialmente, derogada, condicionada, pendiente de control constitucional o discutible.
4. Documente fuente oficial: Corte Constitucional, SUIN-Juriscol, Diario Oficial, Ministerio del Trabajo, Colpensiones, Superfinanciera, UGPP o Funcion Publica.
5. Si usa el Excel `BRECHAS .xlsx`, trate sus formulas como especificacion funcional a descubrir. No reemplace una formula sin entender su intencion.
6. Valide cada motor contra fixtures del Excel o contra casos normativos auditables.
7. Guarde inputs, outputs, version de motor, version de ruleset y normativa usada.

## Ley 2381 de 2024

No asuma vigencia plena. Antes de activar reglas de esa ley, consulte fuentes oficiales actualizadas y documente si la regla esta suspendida, vigente parcialmente, condicionada o pendiente de control constitucional. Trate por separado disposiciones con vigencia independiente.

## Seguros

El diagnostico de seguros debe partir de necesidades del cliente: fallecimiento, invalidez, incapacidad, enfermedades graves, educacion, deudas, ingresos, patrimonio, retiro y dependientes. La brecha se calcula como necesidad economica estimada menos cobertura existente. No hardcodee tarifas comerciales de aseguradoras.
