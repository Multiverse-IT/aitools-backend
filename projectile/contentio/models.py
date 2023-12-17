from django.conf import settings
from django.db import models

from autoslug import AutoSlugField

from versatileimagefield.fields import VersatileImageField

from common.models import BaseModelWithUID

from .choices import PostStatus
from .utils import get_post_media_path_prefix, get_post_slug
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
    is_indexed = models.BooleanField(default=True)
    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    view_count = models.PositiveBigIntegerField(default=0)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}-slug: {self.slug}"


