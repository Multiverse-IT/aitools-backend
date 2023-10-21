from django.db import models

from common.models import BaseModelWithUID

from versatileimagefield.fields import VersatileImageField

from .choices import ToolStatus, ToolKind
from .utils import (
    get_tools_media_path_prefix,
)


class Tool(BaseModelWithUID):
    name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    pricing = models.DecimalField(
        decimal_places=3, max_digits=19, blank=True, null=True
    )
    categories = models.JSONField(default=list, null=False, blank=True)
    description = models.TextField(blank=True)
    slug = models.CharField(max_length=55, unique=True, db_index=True)
    is_editor = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    save_count = models.PositiveBigIntegerField(default=0)
    image = VersatileImageField(
        "Avatar",
        upload_to=get_tools_media_path_prefix,
        blank=True,
    )
    short_description = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=30, choices=ToolStatus.choices, default=ToolStatus.ACTIVE
    )
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    # Links to other external urls
    canonical_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    blog_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Tools"

    def __str__(self):
        return f"UID: {self.uid}, Created: {self.created_at}"


class Rating(BaseModelWithUID):
    slug = models.CharField(max_length=55, unique=True, db_index=True)
    pros = models.CharField(max_length=255, blank=True)
    cons = models.CharField(max_length=255, blank=True)
    review = models.CharField(max_length=255, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=None)

    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    # FK
    # tool = models.ForeignKey(Tool, on_delete=models.CASCADE)

    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    def __str__(self):
        return f"UID: {self.uid}, Tool: {self.tool.name}"

    class Meta:
        ordering = ("created_at",)
        verbose_name_plural = "Ratings"


class Feature(BaseModelWithUID):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=55, unique=True, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    def __str__(self):
        return f"UID: {self.uid}, Title: {self.title}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Features"


class ToolsConnector(BaseModelWithUID):
    slug = models.CharField(max_length=55, unique=True, db_index=True)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, blank=True, null=True)
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, blank=True, null=True
    )
    kind = models.CharField(max_length=30, choices=ToolKind.choices)

    def __str__(self):
        return f"UID: {self.uid}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "ToolsConnector"


class Category(BaseModelWithUID):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=55, unique=True, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    def __str__(self):
        return f"UID: {self.uid}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Categories"


class SubCategory(BaseModelWithUID):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=55, unique=True, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    # FK
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    def __str__(self):
        return f"UID: {self.uid}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Sub Categories"
