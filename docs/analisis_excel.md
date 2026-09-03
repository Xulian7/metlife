# Analisis del Excel `BRECHAS .xlsx`

Archivo localizado: `BRECHAS .xlsx`. No se modifico.

## Hojas

- `DATOS GERERALES`: captura datos del cliente, actividad economica, ingreso, gasto, conyuge, hijos y resumen de compromisos/desprotecciones.
- `PANORAMA LEY 100`: calcula brechas de fallecimiento, invalidez, vejez Colpensiones y vejez fondo privado bajo supuestos del libro.
- `PANORAMA REFORMA`: compara un panorama de reforma/sistema de pilares; por seguridad juridica queda documentado, no activado como regla vigente.
- `EDUCACION HIJOS`: estima necesidad educativa por hijo, acumulacion universitaria y seguro/inversion requerida.

## Inputs observados

- Cliente: nombre `CARLOS CERVANTES`, edad 34, edad esperada de pension 62.
- Actividad economica: medico general.
- Salario/honorarios: COP 4.000.000.
- Gasto mensual: COP 3.000.000.
- Conyuge: campos presentes pero incompletos.
- Hijos: hasta cinco hijos, edad por hijo, pension escolar mensual y costo universitario.
- Parametros: SMMLV COP 1.423.500, factor de capital 200, tasa de renta mensual 0,5%, factor Fedesarrollo 377, semanas por ano 52, aporte de acumulacion 11,5%.

## Outputs principales del caso consistente

- Descobertura educativa total: COP 650.000.000.
- Colegio: COP 408.000.000.
- Universidad: COP 242.000.000.
- Fallecimiento Ley 100: brecha COP 2.785.600; capital COP 557.120.000.
- Invalidez Ley 100: brecha COP 2.838.400; capital COP 567.680.000.
- Vejez Colpensiones Ley 100: brecha COP 2.592.000; capital COP 518.400.000.
- Vejez fondo privado Ley 100: brecha COP 2.747.320; capital COP 549.464.000.

## Formulas reconstruidas

- Pension minima neta Ley 100: `SMMLV * (1 - 12%)`.
- Pension invalidez: si `IBC_10_anios * 66%` supera el minimo neto, aplica `* 88%`; si no, usa minimo neto.
- Pension sobrevivencia: si `IBC_10_anios * 69%` supera el minimo neto, aplica `* 88%`; si no, usa minimo neto.
- Pension Colpensiones: si `IBC_actual * 80% * 87,5%` supera el minimo neto, aplica `IBC_actual * 80% * 88%`; si no, usa minimo neto.
- Capital necesario: `brecha_mensual * 200`.
- Renta mensual esperada: `capital * 0,5%`, que equivale a la brecha mensual.
- Capital Fedesarrollo: `377 * SMMLV`.
- Acumulacion proyectada AFP: `IBC_actual * 11,5% * 12 * anios_totales`.
- Pension privada estimada: `max(SMMLV * (acumulacion/capital_fedesarrollo) * 88%, pension_minima_neta)`.
- Educacion por hijo: `pension_mensual * 12 * anios_hasta_17 + costo_universidad`.

## Alertas del libro

- Hay errores `#VALUE!` en la columna de analisis del conyuge por referencias a celdas vacias o texto `%`.
- La hoja `PANORAMA REFORMA` incluye reglas de reforma que no deben activarse sin estado juridico oficial.
- El nombre de la hoja `DATOS GERERALES` conserva un error ortografico del archivo original.
