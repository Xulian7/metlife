# Consultoria 360 MetLife

Aplicacion interna Django para CRM consultivo, visitas, diagnostico de clientes, seguimiento comercial y simulaciones pensionales/financieras auditables.

Repositorio GitHub para Railway: https://github.com/Xulian7/metlife.git

## Desarrollo local

1. Cree un entorno virtual.
2. Instale dependencias con `pip install -r requirements.txt`.
3. Copie `.env.example` a `.env` y configure variables.
4. Ejecute `python manage.py migrate`.
5. Cree usuario con `python manage.py createsuperuser`.
6. Inicie con `python manage.py runserver`.

Si `DATABASE_URL` no existe, se usa SQLite solo como respaldo de desarrollo. Para desarrollo local puede activar `DEBUG=True`. En Railway y ambientes compartidos use PostgreSQL.

## Comandos utiles

- `python manage.py check`
- `python manage.py test`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py collectstatic --noinput`

La logica financiera, pensional y de seguros vive en servicios de dominio, no en vistas ni plantillas.
