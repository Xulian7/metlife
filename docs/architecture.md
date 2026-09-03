# Arquitectura

La aplicacion usa Django con apps por dominio. `core` contiene dashboard y navegacion; `clientes`, `visitas` y `consultoria` cubren el flujo consultivo; `pensiones`, `seguros` y `simuladores` contienen reglas y motores; `auditoria` centraliza trazabilidad.

El modulo `leads` queda como codigo heredado/no visible por ahora. El producto se enfoca en clientes, reuniones, visitas, estados de relacion y simulaciones.

Las vistas coordinan formularios y permisos, pero no calculan reglas financieras o pensionales. Los motores viven en servicios puros cuando es posible.

PostgreSQL es la base objetivo mediante `DATABASE_URL`. SQLite se permite solo para desarrollo local cuando no existe esa variable.
