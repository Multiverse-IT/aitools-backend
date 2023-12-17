from autoslug import AutoSlugField

from django.db import models
from django.contrib.auth import get_user_model

from versatileimagefield.fields import VersatileImageField

from common.models import BaseModelWithUID

from .choices import RequestToolStatus, ToolKind, ToolStatus
from .utils import (
    get_category_media_path_prefix,
    get_subategory_media_path_prefix,
    get_tools_media_path_prefix,
    get_feature_slug
)
from .managers import ToolQuerySet

User = get_user_model()


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
    alt = models.CharField(max_length=255, blank=True)
    requested = models.BooleanField(default=False)

    is_indexed = models.BooleanField(default=True)
    short_description = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=30, choices=ToolStatus.choices, default=ToolStatus.ACTIVE
    )
    is_featured = models.BooleanField(default=False)
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

    objects = ToolQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Tools"

    def __str__(self):
        return f"Slug: {self.slug}, Created: {self.created_at}"


class Rating(BaseModelWithUID):
    pros = models.CharField(max_length=255, blank=True)
    cons = models.CharField(max_length=255, blank=True)
    review = models.CharField(max_length=255, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=None)

    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    # FKs 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Add this line to link ratings to users

    def __str__(self):
        return f"UID: {self.uid}"

    class Meta:
        ordering = ("created_at",)
        verbose_name_plural = "Ratings"


class Feature(BaseModelWithUID):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=55, unique=True, db_index=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    is_indexed = models.BooleanField(default=True)
    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    def __str__(self):
        return f"Slug: {self.slug}, Title: {self.title}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Features"


class ToolsConnector(BaseModelWithUID):
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
    image = VersatileImageField(
        "Avatar",
        upload_to=get_category_media_path_prefix,
        blank=True,
    )
    alt = models.CharField(max_length=255, blank=True)
    is_indexed = models.BooleanField(default=True)
    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    def __str__(self):
        return f"Slug: {self.slug}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Categories"


class SubCategory(BaseModelWithUID):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=55, unique=True, db_index=True)
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    image = VersatileImageField(
        "Avatar",
        upload_to=get_subategory_media_path_prefix,
        blank=True,
    )
    alt = models.CharField(max_length=255, blank=True)
    is_indexed = models.BooleanField(default=True)

    # Links to other external urls
    canonical_url = models.URLField(blank=True)

    def __str__(self):
        return f"Slug: {self.slug}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Sub Categories"


class ToolsCategoryConnector(BaseModelWithUID):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Category connectors"


class SavedTool(BaseModelWithUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    love_tool = models.ForeignKey(
        Tool, on_delete=models.SET_NULL, null=True, blank=True, related_name="love_tool"
    )
    save_tool = models.ForeignKey(
        Tool, on_delete=models.SET_NULL, null=True, blank=True, related_name="save_tool"
    )

    def __str__(self):
        return f"USER: {self.user.get_name()}"


class ToolRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    status = models.CharField(
        choices=RequestToolStatus.choices,
        default=RequestToolStatus.PENDING,
        max_length=30,
    )

    def __str__(self):
        return f"User: {self.user.get_name()}-Tool: {self.tool.name}"
    


class FeatureTool(BaseModelWithUID):
    slug = AutoSlugField(populate_from=get_feature_slug, unique=True, db_index=True)
    tool = models.JSONField(default=list, null=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"UID: {self.uid}-SLUG: {self.slug}"