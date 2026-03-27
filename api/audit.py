from core.models import AuditLog


class AuditLogMixin:
    def _write_audit(self, action, instance=None):
        actor = self.request.user.username if self.request.user.is_authenticated else "anonymous"
        school_id = getattr(instance, "school_id", None)
        entity = instance.__class__.__name__ if instance is not None else self.__class__.__name__
        entity_id = str(getattr(instance, "pk", "")) if instance is not None else ""
        AuditLog.objects.create(
            school_id=school_id,
            actor=actor,
            action=action,
            entity=entity,
            entity_id=entity_id,
            metadata={"path": self.request.path, "method": self.request.method},
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        self._write_audit("create", instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._write_audit("update", instance)

    def perform_destroy(self, instance):
        self._write_audit("delete", instance)
        instance.delete()
