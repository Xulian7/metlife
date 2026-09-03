# Simulador

Motor inicial: `pensiones.services.calcular_panorama_ley_100`, `pensiones.services.calcular_panorama_reforma` y `simuladores.services.run_excel_brechas_basico`.

Estado: parcial, basado en el caso principal consistente del Excel. Guarda inputs y outputs con version de motor `0.2.0` y ruleset `colombia-pensiones-2026-09-borrador`.

La interfaz de simulacion ahora trabaja con dos escenarios equivalentes a pestanas del Excel:

- Panorama Ley 100.
- Panorama Reforma, marcado como escenario consultivo sin vigencia juridica plena por defecto.

Pendiente: convertir mas escenarios del Excel en fixtures, resolver errores de la columna conyuge y formalizar un mapa completo de formulas antes de activar nuevas reglas.
