from django.db import models


class PostStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"
