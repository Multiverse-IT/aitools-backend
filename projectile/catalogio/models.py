from autoslug import AutoSlugField
from common.models import BaseModelWithUID
from django.db import models
from versatileimagefield.fields import VersatileImageField

from .utils import get_tool_slug, get_tools_media_path_prefix


class Tool(BaseModelWithUID):
    name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    pricing = models.DecimalField(
        decimal_places=3, max_digits=19, blank=True, null=True
    )
    categories = models.JSONField(default=list, null=False, blank=True)
    description = models.TextField()
    slug = AutoSlugField(populate_from=get_tool_slug, unique=True, db_index=True)
    is_editor = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    save = models.PositiveBigIntegerField()
    image = VersatileImageField(
        "Avatar",
        upload_to=get_tools_media_path_prefix,
        blank=True,
    )
    short_description = models.CharField(max_length=255)

    # Links to other external urls
    website_url = models.URLField(blank=True)
    blog_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return (
            f"UID: {self.uid}, Verified:{self.is_verified}, Created: {self.created_at}"
        )


class Rating(BaseModelWithUID):
    pros = models.CharField(max_length=255, blank=True)
    cons = models.CharField(max_length=255, blank=True)
    review = models.CharField(max_length=255, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=None)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)

    def __str__(self):
        return f"UID: {self.uid}, Tool: {self.tool.name}"

    class Meta:
        ordering = ("created_at",)


class Feature(BaseModelWithUID):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"UID: {self.uid}, Title: {self.title}"

    class Meta:
        ordering = ("created_at",)


class ToolsConnector(BaseModelWithUID):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, blank=True, null=True)
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"UID: {self.uid}"


class Category(BaseModelWithUID):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"UID: {self.uid}"


class SubCategory(BaseModelWithUID):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"UID: {self.uid}"


class CategoryConnector(BaseModelWithUID):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"UID: {self.uid}"
