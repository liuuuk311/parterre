from datetime import datetime

from django.db.models import QuerySet


class TimestampedQuerySet(QuerySet):
    def mark_as_deleted(self):
        self.update(deleted_at=datetime.utcnow())

    def only_active(self):
        return self.filter(deleted_at__isnull=True)
