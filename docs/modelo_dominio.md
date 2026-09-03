# Modelo de dominio

Entidades principales:

- `ConsultantProfile`: rol operativo del usuario.
- `Cliente`: perfil progresivo del cliente/prospecto.
- `Consentimiento`: autorizacion de tratamiento de datos.
- `ClienteEstado`: estado configurable de la relacion consultiva.
- `ClienteEstadoHistory`: trazabilidad de cambio de estado del cliente.
- `SeguimientoCliente`: compromiso o accion futura asociada directamente al cliente.
- `Visita`: registro central de visita.
- `ConsultoriaCaso`: diagnostico guiado por secciones.
- `Simulacion`: snapshot auditable de inputs, outputs y versiones.
- `NormativaPensional` y `PensionRule`: reglas juridicas versionadas.
- `FondoPensiones`: administradora y regimen pensional detectado.
- `DiagnosticoProteccion` y `CoberturaExistente`: necesidades y brechas de seguros.
- `Producto`: catalogo parametrizable.
- `AuditLog`: trazabilidad general.
- `TimelineEvent`: relacion comercial cronologica del cliente.
