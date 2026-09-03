# Railway

Repositorio fuente: https://github.com/Xulian7/metlife.git

Variables requeridas:

- `SECRET_KEY`
- `DEBUG=False`
- `DATABASE_URL`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `PGSSLMODE=require`

El archivo `nixpacks.toml` crea un entorno virtual en `/opt/venv`, instala dependencias desde `requirements.txt`, ejecuta `collectstatic` en build y arranca con migraciones + Gunicorn desde ese entorno. En produccion use PostgreSQL de Railway y no guarde secretos en el repositorio.

Gunicorn debe escuchar en `0.0.0.0:$PORT`; Railway no expone aplicaciones que se quedan en el puerto local por defecto.
