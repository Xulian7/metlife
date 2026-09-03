# Reglas de negocio iniciales

## Clientes y seguimiento

- Un prospecto o cliente se modela como `Cliente`.
- Los estados de relacion son configurables en `ClienteEstado`.
- Los cambios de estado se guardan en `ClienteEstadoHistory`; no se sobrescribe el historial.
- Seguimientos, reuniones, visitas, simulaciones y diagnosticos alimentan el timeline del cliente.
- La seleccion de fondo pensional permite detectar regimen: Colpensiones/RPM, AFP privada/RAIS o ACCAI especial.

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
