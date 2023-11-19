from django.db import models

from catalogio.choices import ToolStatus


class ToolQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=ToolStatus.ACTIVE)

    def get_status_requested(self):
        return self.filter(requested=True)

    def get_status_editable(self):
        statuses = [ToolStatus.PENDING, ToolStatus.ACTIVE, ToolStatus.DRAFT]
        return self.filter(status__in=statuses)
