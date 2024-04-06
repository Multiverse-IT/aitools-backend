from django.contrib import admin
from django import forms

from .models import (
    Category,
    Feature,
    Rating,
    SubCategory,
    Tool,
    ToolsConnector,
    ToolsCategoryConnector,
    ToolRequest,
    SavedTool,
    FeatureTool,
    TopHundredTools,
    BestAlternativeTool,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["title"]


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ["uid", "id", "name","slug", "created_at"]
    search_fields = ["name"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    search_fields = ["title"]


@admin.register(ToolsCategoryConnector)
class ToolsCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]


@admin.register(ToolsConnector)
class ToolsConnectorAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]

class FeatureAdminForm(forms.ModelForm):
    class Meta:
        model = Feature
        exclude = []

class FeatureAdmin(admin.ModelAdmin):
    form = FeatureAdminForm

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    search_fields = ["title"]


admin.site.register(ToolRequest)
admin.site.register(SavedTool)
admin.site.register(FeatureTool)
admin.site.register(TopHundredTools)
admin.site.register(BestAlternativeTool)