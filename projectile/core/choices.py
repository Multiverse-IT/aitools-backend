from django.db import models


class UserGender(models.TextChoices):
    FEMALE = "FEMALE", "Female"
    MALE = "MALE", "Male"
    OTHER = "OTHER", "Other"


class UserStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PLACEHOLDER = "PLACEHOLDER", "Placeholder"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    PAUSED = "PAUSED", "Paused"
    REMOVED = "REMOVED", "Removed"


class UserRole(models.TextChoices):
    INITIATOR = "INITIATOR", "Initiator"
    STAFF = "STAFF", "Staff"
    ADMIN = "ADMIN", "Admin"
    OWNER = "OWNER", "Owner"
