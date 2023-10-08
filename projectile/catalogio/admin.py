from django.contrib import admin

from .models import (
    Category,
    CategoryConnector,
    Feature,
    Rating,
    SubCategory,
    Tool,
    ToolsConnector,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["title"]


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    search_fields = ["name"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    search_fields = ["title"]


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    search_fields = ["title"]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]


@admin.register(CategoryConnector)
class CategoryConnectorAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]


@admin.register(ToolsConnector)
class ToolsConnectorAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]
