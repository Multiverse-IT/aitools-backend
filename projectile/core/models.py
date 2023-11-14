from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField

from common.models import BaseModelWithUID

from phonenumber_field.modelfields import PhoneNumberField

from versatileimagefield.fields import VersatileImageField

from .choices import UserGender, UserStatus, UserRole
from .managers import CustomUserManager
from .utils import get_user_media_path_prefix, get_user_slug


class User(AbstractUser, BaseModelWithUID):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    email = models.EmailField(unique=True, db_index=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, db_index=True)
    language = models.CharField(max_length=2, default="en")
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    slug = AutoSlugField(populate_from=get_user_slug, unique=True, db_index=True)
    avatar = VersatileImageField(
        "Avatar",
        upload_to=get_user_media_path_prefix,
        blank=True,
    )
    image = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        db_index=True,
        default=UserStatus.DRAFT,
    )
    gender = models.CharField(
        max_length=20, blank=True, null=True, choices=UserGender.choices, db_index=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(
        max_length=30, choices=UserRole.choices, default=UserRole.INITIATOR
    )
    # extra field for google auth 
    exp = models.CharField(max_length=255, blank=True)
    sub = models.CharField(max_length=255, blank=True)
    iat = models.CharField(max_length=255, blank=True)
    jti = models.CharField(max_length=255, blank=True)
    picture = models.CharField(max_length=255,blank=True)
    # Other links
    website_url = models.URLField(blank=True)
    blog_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"ID: {self.id}, Email: {self.email}"

    def get_name(self):
        name = " ".join([self.first_name, self.last_name])
        return name.strip()

    def activate(self):
        self.is_active = True
        self.status = UserStatus.ACTIVE
        self.save_dirty_fields()
