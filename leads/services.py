from django.contrib.auth import get_user_model
from django.db import transaction

from clientes.services import record_timeline_event

from .models import Lead, LeadStageHistory, PipelineStage

User = get_user_model()

DEFAULT_PIPELINE = [
    "Nuevo", "Por contactar", "Contactado", "Cita agendada", "Visitado",
    "Diagnostico realizado", "Propuesta pendiente", "Propuesta presentada",
    "Documentacion", "Seguimiento", "Ganado", "Perdido", "No interesado",
]


def ensure_default_pipeline() -> None:
    for order, name in enumerate(DEFAULT_PIPELINE, start=1):
        PipelineStage.objects.get_or_create(nombre=name, defaults={"orden": order, "es_cierre": name in {"Ganado", "Perdido", "No interesado"}})


@transaction.atomic
def change_lead_stage(*, lead: Lead, new_stage: PipelineStage, actor: User | None, note: str = "") -> LeadStageHistory:
    previous = lead.etapa
    if previous_id := getattr(previous, "id", None):
        if previous_id == new_stage.id:
            return LeadStageHistory.objects.create(lead=lead, from_stage=previous, to_stage=new_stage, changed_by=actor, note=note)
    lead.etapa = new_stage
    lead.save(update_fields=["etapa", "actualizado_en"])
    history = LeadStageHistory.objects.create(lead=lead, from_stage=previous, to_stage=new_stage, changed_by=actor, note=note)
    record_timeline_event(
        cliente=lead.cliente,
        actor=actor,
        tipo="lead",
        titulo=f"Lead movido a {new_stage.nombre}",
        descripcion=note,
        object_label=str(lead),
    )
    return history
