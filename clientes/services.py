from django.contrib.auth import get_user_model

from .models import Cliente, ClienteEstado, ClienteEstadoHistory, SeguimientoCliente, TimelineEvent

User = get_user_model()


def record_timeline_event(
    *,
    cliente: Cliente,
    actor: User | None,
    tipo: str,
    titulo: str,
    descripcion: str = "",
    object_label: str = "",
    metadata: dict | None = None,
) -> TimelineEvent:
    return TimelineEvent.objects.create(
        cliente=cliente,
        actor=actor,
        tipo=tipo,
        titulo=titulo,
        descripcion=descripcion,
        object_label=object_label,
        metadata=metadata or {},
    )


DEFAULT_CLIENT_STATES = [
    ("Nuevo", "azul"),
    ("Contactado", "cyan"),
    ("Reunion agendada", "verde"),
    ("Visitado", "morado"),
    ("Diagnostico en curso", "ambar"),
    ("Simulacion realizada", "azul"),
    ("Propuesta por preparar", "ambar"),
    ("Seguimiento activo", "verde"),
    ("Cliente activo", "verde"),
    ("Pausado", "gris"),
    ("Cerrado", "gris"),
]


def ensure_default_client_states() -> None:
    for order, (name, color) in enumerate(DEFAULT_CLIENT_STATES, start=1):
        ClienteEstado.objects.get_or_create(nombre=name, defaults={"orden": order, "color": color})


def change_cliente_estado(*, cliente: Cliente, new_estado: ClienteEstado, actor: User | None, note: str = "") -> ClienteEstadoHistory:
    previous = cliente.estado_relacion
    cliente.estado_relacion = new_estado
    cliente.save(update_fields=["estado_relacion", "actualizado_en"])
    history = ClienteEstadoHistory.objects.create(cliente=cliente, from_estado=previous, to_estado=new_estado, changed_by=actor, note=note)
    record_timeline_event(cliente=cliente, actor=actor, tipo="estado", titulo=f"Estado cambiado a {new_estado.nombre}", descripcion=note)
    return history


def create_cliente_followup(*, cliente: Cliente, consultor: User, fecha, tipo: str, objetivo: str = "", notas: str = "") -> SeguimientoCliente:
    seguimiento = SeguimientoCliente.objects.create(cliente=cliente, consultor=consultor, fecha=fecha, tipo=tipo, objetivo=objetivo, notas=notas)
    record_timeline_event(cliente=cliente, actor=consultor, tipo="seguimiento", titulo=f"Seguimiento programado: {tipo}", descripcion=objetivo or notas)
    return seguimiento
