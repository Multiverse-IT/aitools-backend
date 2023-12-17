from django.db import models

from .choices import PostStatus



class PostQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=PostStatus.ACTIVE)

    def get_status_requested(self):
        return self.filter(requested=True)

    def get_status_editable(self):
        statuses = [PostStatus.ACTIVE, PostStatus.DRAFT]
        return self.filter(status__in=statuses)
