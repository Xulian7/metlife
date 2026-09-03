from .models import AuditLog


def audit(*, actor, action: str, obj, summary: str = "", changes: dict | None = None) -> AuditLog:
    return AuditLog.objects.create(
        actor=actor,
        action=action,
        object_type=obj.__class__.__name__,
        object_id=str(getattr(obj, "pk", "")),
        summary=summary,
        changes=changes or {},
    )
