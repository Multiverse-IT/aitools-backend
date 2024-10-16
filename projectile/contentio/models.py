from django.conf import settings
from django.db import models

from autoslug import AutoSlugField

from versatileimagefield.fields import VersatileImageField

from common.models import BaseModelWithUID

from .choices import PostStatus
from .utils import get_post_media_path_prefix, get_post_slug, get_faq_media_path_prefix
from .managers import PostQuerySet


class Post(BaseModelWithUID):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from=get_post_slug, unique=True, db_index=True)
    avatar = VersatileImageField(
        "Image",
        upload_to=get_post_media_path_prefix,
        blank=True,
    )
    alt = models.CharField(max_length=255, blank=True)

    status = models.CharField(
        max_length=20,
        choices=PostStatus.choices,
        db_index=True,
        default=PostStatus.ACTIVE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    is_noindex = models.BooleanField(default=False)
    focus_keyword = models.CharField(max_length=255, blank=True)

    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    view_count = models.PositiveBigIntegerField(default=0)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}-slug: {self.slug}"


class CommonStorage(BaseModelWithUID):
    storage = models.JSONField(default=list)
    home_page = models.JSONField(default=list)
    categories_page = models.JSONField(default=list)
    blogs_page = models.JSONField(default=list)
    about_page = models.JSONField(default=list)
    redirects = models.JSONField(default=list)
    privacy_policy = models.JSONField(default=list)
    terms_of_use = models.JSONField(default=list)

    def __str__(self) -> str:
        return f"UID: {self.uid}"


class Redirect(BaseModelWithUID):
    type = models.CharField(max_length=255, blank=True)
    is_permanent = models.BooleanField(default=False)
    old = models.CharField(max_length=255, blank=True)
    new = models.CharField(max_length=255, blank=True)
    extras = models.JSONField(default=list)

    def __str__(self):
        return f"ID: {self.id}"


class Sponsor(BaseModelWithUID):
    field = models.JSONField(default=list)
    nofollow = models.BooleanField(default=False)
    dofollow = models.BooleanField(default=False)

    def __str__(self):
        return f"UID: {self.uid}"


class FAQ(BaseModelWithUID):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from=get_post_slug, unique=True, db_index=True)
    summary = models.TextField(blank=True)
    priority = models.IntegerField(
        default=0, help_text="Higher number is higher priority."
    )

    def __str__(self):
        return f"UID: {self.uid} - Title: {self.title}"

class FaqCategoryConnector(BaseModelWithUID):
    faq = models.ForeignKey(FAQ, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey("catalogio.SubCategory", on_delete=models.CASCADE, blank=True, null=True)
