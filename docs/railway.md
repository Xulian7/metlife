# Railway

Repositorio fuente: https://github.com/Xulian7/metlife.git

Variables requeridas:

- `SECRET_KEY`
- `DEBUG=False`
- `DATABASE_URL`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `PGSSLMODE=require`

El archivo `railway.json` ejecuta migraciones, collectstatic y Gunicorn en el arranque. En produccion use PostgreSQL de Railway y no guarde secretos en el repositorio.
