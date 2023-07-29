import uuid
from datetime import datetime

from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None, blank=True)

    class Meta:
        abstract = True

    def mark_as_deleted(self, commit=True):
        self.deleted_at = datetime.utcnow()
        if commit:
            self.save()


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, "name"):
            return f"{self.name}"

        return f"{self.__class__.__name__} ({self.code})"

    @property
    def code(self):
        return self.id.int & (1 << 18) - 1
