from django.db import models


class ToolStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    REMOVED = "REMOVED", "Removed"


class ToolKind(models.TextChoices):
    FEATURE = "FEATUER", "Feature"
    RATING = "RATING", "Rating"


class RequestToolStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
