---
name: corporate-ui-ux
description: Especialista senior en UI/UX corporativo para aplicaciones web internas, dashboards, tablas, CRUD, CRM, formularios, filtros y sistemas administrativos. Usar al crear, modificar o revisar interfaces empresariales.
---

# Corporate UI/UX

Use esta skill para mejorar interfaces corporativas sin cambiar innecesariamente el stack del proyecto.

## Principios

- Priorice claridad, jerarquia, velocidad de uso, consistencia, densidad controlada y estetica.
- No convierta una aplicacion empresarial en landing page.
- Reutilice el sistema existente: templates Django, CSS compartido, componentes, colores, sidebar, tablas y formularios.
- Use el color corporativo como acento, no como fondo dominante.
- Mantenga interfaces densas pero legibles; el usuario debe poder ver, entender, decidir y actuar rapido.
- Centralice patrones visuales en CSS compartido antes de crear estilos aislados por pantalla.

## Formularios

- Agrupe campos por significado, no como una lista plana.
- Mantenga labels visibles.
- Muestre validaciones junto al campo.
- En datos monetarios, deje clara la moneda, precision y significado.
- En selects grandes, use busqueda o autocomplete si la cantidad de opciones crece.

## Tablas

- Las tablas deben facilitar lectura, comparacion, busqueda, filtrado, acciones rapidas y toma de decisiones.
- Alinee texto a la izquierda, fechas al centro y cantidades/moneda a la derecha cuando aplique.
- Use numeros tabulares para comparacion.
- Reserve badges para estados o clasificaciones reales.
- Para tablas largas, considere header sticky y paginacion informativa.

## Dashboards

- Cada KPI debe responder una pregunta de negocio.
- Use estructura: encabezado, filtros, KPIs, tendencias o distribuciones y tabla operativa.
- Evite graficos decorativos; cada grafico debe explicar una decision.

## Accesibilidad y responsive

- Mantenga contraste, foco visible, navegacion por teclado, labels y semantica HTML.
- No dependa solo del color para comunicar estados.
- Verifique escritorio, laptop, tablet y movil.

## Criterio de terminado

Una pantalla esta lista cuando se entiende donde esta el usuario, que puede hacer, que datos importan, como corregir errores y como continuar el flujo sin perder contexto.
