# Modelo de dominio

Entidades principales:

- `ConsultantProfile`: rol operativo del usuario.
- `Cliente`: perfil progresivo del cliente/prospecto.
- `Consentimiento`: autorizacion de tratamiento de datos.
- `PipelineStage`: etapa comercial configurable.
- `Lead`: oportunidad comercial.
- `LeadStageHistory`: trazabilidad de etapa.
- `Seguimiento`: compromiso o accion futura.
- `Visita`: registro central de visita.
- `ConsultoriaCaso`: diagnostico guiado por secciones.
- `Simulacion`: snapshot auditable de inputs, outputs y versiones.
- `NormativaPensional` y `PensionRule`: reglas juridicas versionadas.
- `DiagnosticoProteccion` y `CoberturaExistente`: necesidades y brechas de seguros.
- `Producto`: catalogo parametrizable.
- `AuditLog`: trazabilidad general.
- `TimelineEvent`: relacion comercial cronologica del cliente.
