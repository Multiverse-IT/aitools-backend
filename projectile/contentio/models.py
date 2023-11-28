from django.db import models

from autoslug import AutoSlugField
from common.models import BaseModelWithUID
from versatileimagefield.fields import VersatileImageField

from .utils import get_post_slug, get_post_media_path_prefix
from .choices import PostStatus

class Post(BaseModelWithUID):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from=get_post_slug, unique=True, db_index=True)
    avatar = VersatileImageField(
        "Image",
        upload_to=get_post_media_path_prefix,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=PostStatus.choices,
        db_index=True,
        default=PostStatus.ACTIVE,
    )

    def __str__(self):
        return f"UID: {self.uid}-slug: {self.slug}"