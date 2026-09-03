from django.contrib.auth import get_user_model

from .models import Cliente, TimelineEvent

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
