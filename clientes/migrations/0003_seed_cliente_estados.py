from django.db import migrations


ESTADOS = [
    ("Nuevo", 1, "azul"),
    ("Contactado", 2, "cyan"),
    ("Reunion agendada", 3, "verde"),
    ("Visitado", 4, "morado"),
    ("Diagnostico en curso", 5, "ambar"),
    ("Simulacion realizada", 6, "azul"),
    ("Propuesta por preparar", 7, "ambar"),
    ("Seguimiento activo", 8, "verde"),
    ("Cliente activo", 9, "verde"),
    ("Pausado", 10, "gris"),
    ("Cerrado", 11, "gris"),
]


def seed(apps, schema_editor):
    ClienteEstado = apps.get_model("clientes", "ClienteEstado")
    for nombre, orden, color in ESTADOS:
        ClienteEstado.objects.get_or_create(nombre=nombre, defaults={"orden": orden, "color": color, "activo": True})


class Migration(migrations.Migration):
    dependencies = [("clientes", "0002_clienteestado_cliente_conyuge_fecha_nacimiento_and_more")]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
