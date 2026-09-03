# AGENTS.md

Objetivo: construir una herramienta interna de consultoria 360 para clientes, leads, visitas, diagnosticos, seguros y simulaciones pensionales/financieras auditables.

Arquitectura: Django modular con apps `accounts`, `clientes`, `leads`, `visitas`, `consultoria`, `pensiones`, `seguros`, `simuladores`, `productos`, `auditoria` y `core`.

Reglas de dominio: ubicar calculos y decisiones en `pensiones/services.py`, `seguros/services.py`, `simuladores/services.py` o submodulos equivalentes. No poner reglas financieras o pensionales en views/templates.

Fuentes de verdad: Excel original `BRECHAS .xlsx`, PDFs de clausulados, documentos en `docs/`, normativa oficial y tests de equivalencia.

Simulador: toda simulacion debe guardar inputs, outputs, version de motor y version de ruleset. No recalcular historicos silenciosamente.

Normativa: antes de modificar reglas pensionales, verificar fuentes oficiales y documentar fuente, vigencia, estado juridico y supuesto.

Tests obligatorios: cambios en modelos, pipeline, visitas, permisos, simulador o reglas deben incluir o actualizar pruebas. Comandos: `python manage.py check` y `python manage.py test`.

Convenciones: usar `Decimal` para dinero, zona horaria `America/Bogota`, nombres descriptivos, consultas con `select_related`/`prefetch_related` cuando aplique y migraciones revisadas.

Criterio de terminado: migraciones creadas, `check` sin errores, tests verdes, documentacion actualizada y sin secretos reales en el repositorio.
