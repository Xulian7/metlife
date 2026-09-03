# Analisis de documentos de negocio

No se encontro documento Word (`.docx` o `.doc`) en el repositorio.

Documentos PDF encontrados:

- `CLAUSULADOS AP .pdf`: poliza de accidentes personales individuales, condiciones generales, codigos de clausulado y nota tecnica.
- `CLAUSULADOS ECO BIENESTAR .pdf`: seguro de proteccion Ecosistema de Bienestar, condiciones generales, cobertura basica de fallecimiento y coberturas adicionales.

## Entidades extraidas

- Tomador.
- Asegurado.
- Beneficiario.
- Compania aseguradora.
- Poliza.
- Cobertura basica.
- Cobertura adicional.
- Prima.
- Valor asegurado.
- Exclusiones.
- Terminacion.
- Declaracion de beneficiarios.

## Procesos y reglas funcionales extraidas

- Una visita debe capturar necesidades de fallecimiento, invalidez, educacion, ingresos, deudas y dependientes.
- El diagnostico de seguros debe comparar necesidad economica contra cobertura existente.
- Los clausulados son fuentes de condiciones contractuales y exclusiones, no fuentes para hardcodear tarifas comerciales.
- Las exclusiones y limitaciones deben mostrarse como advertencias/documentos asociados, no como diagnostico juridico automatico.

## Riesgos

- Falta el Word descrito por el usuario; las reglas de proceso comercial deben completarse cuando sea aportado.
- La extraccion de PDF fue textual y parcial para la primera version; una revision funcional completa debe hacerse antes de parametrizar productos reales.
