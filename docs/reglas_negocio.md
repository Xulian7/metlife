# Reglas de negocio iniciales

## CRM

- Un prospecto se modela como `Cliente` con estado `prospecto`.
- Un `Lead` debe pertenecer a un cliente/prospecto y a un consultor.
- Las etapas del pipeline son configurables en `PipelineStage`.
- Los cambios de etapa se guardan en `LeadStageHistory`; no se sobrescribe el historial.
- Seguimientos, visitas, simulaciones y diagnosticos alimentan el timeline del cliente.

## Simulaciones

- Inputs y resultados se guardan por separado.
- Cada simulacion conserva `version_motor` y `normativa_version`.
- Resultados historicos no deben recalcularse silenciosamente si cambian reglas futuras.
- Dinero y porcentajes se calculan con `Decimal`, no `float`.

## Pensiones

- Toda regla juridica debe tener fuente, estado juridico y vigencia.
- La Ley 2381 de 2024 no se trata como vigente plenamente por defecto.
- Reglas suspendidas, condicionadas o discutibles solo pueden participar si el ruleset las activa expresamente para una fecha de simulacion.
- Los calculos son simulaciones de consultoria; no son reconocimiento oficial de pension.

## Seguros

- Brecha de proteccion = necesidad economica estimada - cobertura existente.
- No se hardcodean tarifas de aseguradoras.
- Productos y clausulados se parametrizan en catalogos/documentos.
