from django.db import migrations


FONDOS = [
    ("Colpensiones", "rpm", "Administradora Colombiana de Pensiones", "https://www.colpensiones.gov.co/pensiones/publicaciones/120/que-es-el-rpm/", "Administradora estatal del Regimen de Prima Media."),
    ("Porvenir", "rais", "Sociedad Administradora de Fondos de Pensiones y Cesantias", "https://www.superfinanciera.gov.co/publicaciones/38635/pensiones-cesantas-y-fiduciarias-38635/", "AFP privada vigilada por la Superintendencia Financiera."),
    ("Proteccion", "rais", "Administradora de Fondos de Pensiones y Cesantias Proteccion", "https://www.superfinanciera.gov.co/publicaciones/38635/pensiones-cesantas-y-fiduciarias-38635/", "AFP privada vigilada por la Superintendencia Financiera."),
    ("Colfondos", "rais", "Colfondos S.A. Pensiones y Cesantias", "https://www.superfinanciera.gov.co/publicaciones/38635/pensiones-cesantas-y-fiduciarias-38635/", "AFP privada vigilada por la Superintendencia Financiera."),
    ("Skandia Pensiones y Cesantias", "rais", "Skandia Pensiones y Cesantias S.A.", "https://www.superfinanciera.gov.co/publicaciones/38635/pensiones-cesantas-y-fiduciarias-38635/", "AFP privada vigilada por la Superintendencia Financiera."),
    ("Positiva Compania de Seguros", "accai", "Positiva Compania de Seguros S.A.", "https://www.superfinanciera.gov.co/publicaciones/10115449/pensiones-ley-2381-de-2024/", "Autorizada por la SFC como ACCAI; no tratar como AFP tradicional ni activar reglas Ley 2381 sin revisar vigencia."),
]


def seed(apps, schema_editor):
    FondoPensiones = apps.get_model("pensiones", "FondoPensiones")
    for nombre, regimen, entidad, fuente, observaciones in FONDOS:
        FondoPensiones.objects.get_or_create(
            nombre=nombre,
            defaults={"regimen": regimen, "entidad": entidad, "fuente": fuente, "observaciones": observaciones, "activo": True},
        )


class Migration(migrations.Migration):
    dependencies = [("pensiones", "0002_fondopensiones")]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
