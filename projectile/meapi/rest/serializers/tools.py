from django.contrib.auth import get_user_model

from catalogio.choices import ToolKind, ToolStatus
from catalogio.models import (
    Category,
    SavedTool,
    SubCategory,
    Tool,
    ToolRequest,
    ToolsCategoryConnector,
    ToolsConnector,
    Feature
)
from common.serializers import (
    CategorySlimSerializer,
    FeatureSlimSerializer,
    SubCategorySlimSerializer,
    RatingSlimSerializer
)
from rest_framework import serializers

User = get_user_model()

class PublicToolListSerializer(serializers.ModelSerializer):
    feature_slugs = serializers.ListField(
        write_only=True, required=False, child=serializers.CharField()
    )
    category_slug = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
        allow_null = True,
        allow_empty=True
    )
    subcategory_slugs = serializers.ListField(
        write_only=True, required=False, child=serializers.CharField(),  allow_null = True, allow_empty=True
    )
    category = CategorySlimSerializer(
        source="toolscategoryconnector_set.first", read_only=True
    )
    sub_category = SubCategorySlimSerializer(
        source="toolscategoryconnector_set", many=True, read_only=True
    )
    feature = FeatureSlimSerializer(
        source="toolsconnector_set", many=True, read_only=True
    )
    ratings = RatingSlimSerializer(source="toolsconnector_set", many=True, read_only=True)
    average_ratings = serializers.FloatField(read_only=True)
    is_loved = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tool
        fields = [
            "slug",
            "name",
            "is_verified",
            "pricing",
            "categories",
            "description",
            "is_editor",
            "is_trending",
            "is_new",
            "is_loved",
            "is_featured",
            "save_count",
            "meta_title",
            "meta_description",
            "image",
            "requested",
            "is_indexed",
            "feature_slugs",
            "feature",
            "status",
            "ratings",
            "average_ratings",
            "short_description",
            "category_slug",
            "category",
            "subcategory_slugs",
            "sub_category",
            "canonical_url",
            "website_url",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "created_at",
        ]

        read_only_fields = ["uid", "status","requested", "created_at"]
    
    def get_is_loved(self, instance):
        identity = self.context["request"].headers.get("identity")
        user = User.objects.filter(id=identity).first()

        if user:
            return SavedTool.objects.filter(user = user, save_tool = instance).exists()
        else:
            return False
        

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Filter out empty features
        data['feature'] = [feature for feature in data['feature'] if feature]

        # Filter out empty ratings
        data['ratings'] = [rating for rating in data['ratings'] if rating]

        return data
    
    def create(self, validated_data):
        identity = self.context["request"].headers.get("identity")
        user = User.objects.filter(id=identity).first()

        if not user:
            raise serializers.ValidationError({'detail': 'User not found.'})

        feature_slugs = validated_data.pop("feature_slugs", None)
        category = validated_data.pop("category_slug", None)
        subcategory_slugs = validated_data.pop("subcategory_slugs", [])

        tool = Tool.objects.create(requested=True, status=ToolStatus.PENDING, **validated_data)
        
        if tool.requested == True:
            ToolRequest.objects.create(tool=tool, user=user)

        if feature_slugs:
            self._extracted_from_update_9(feature_slugs, tool)

        if category:
            try:
                ToolsCategoryConnector.objects.create(tool=tool, category=category)

                if subcategory_slugs:
                    subcategories = SubCategory.objects.filter(slug__in=subcategory_slugs)
                    for subcategory in subcategories:
                        ToolsCategoryConnector.objects.create(tool=tool, category=category, subcategory=subcategory)
            
            except Category.DoesNotExist:
                print("Category not found")

            except SubCategory.DoesNotExist:
                print("Subcategory not found")

        return tool

    def _extracted_from_update_9(self, feature_slugs, tool):
        feature_connectors = tool.toolsconnector_set.filter(
            feature__isnull=False
        ).delete()

        connectors = [
            ToolsConnector(
                tool=tool,
                feature=Feature.objects.filter(slug=slug).first(),
                kind=ToolKind.FEATURE,
            )
            for slug in feature_slugs
        ]
        ToolsConnector.objects.bulk_create(connectors)



class PublicTooDetailSerializer(serializers.ModelSerializer):
    category = CategorySlimSerializer(
        source="toolscategoryconnector_set.first", read_only=True
    )
    sub_category = SubCategorySlimSerializer(
        source="toolscategoryconnector_set", many=True, read_only=True
    )
    feature = FeatureSlimSerializer(
        source="toolsconnector_set", many=True, read_only=True
    )
    ratings = RatingSlimSerializer(source="toolsconnector_set", many=True, read_only=True)
    average_ratings = serializers.FloatField(read_only=True)
    is_loved = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tool
        fields = [
            "slug",
            "name",
            "is_verified",
            "pricing",
            "categories",
            "description",
            "is_editor",
            "is_trending",
            "is_new",
            "is_featured",
            "is_loved",
            "save_count",
            "meta_title",
            "meta_description",
            "image",
            "is_indexed",
            "feature",
            "status",
            "ratings",
            "average_ratings",
            "short_description",
            "category",
            "sub_category",
            "canonical_url",
            "website_url",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "created_at",
        ]

        read_only_fields = [
            "slug",
            "name",
            "is_verified",
            "pricing",
            "categories",
            "description",
            "is_editor",
            "is_trending",
            "is_new",
            "is_featured",
            "meta_title",
            "meta_description",
            "image",
            "is_indexed",
            "feature",
            "status",
            "short_description",
            "category",
            "sub_category",
            "canonical_url",
            "website_url",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "created_at",
        ]

    def get_is_loved(self, instance):
        identity = self.context["request"].headers.get("identity")
        user = User.objects.filter(id=identity).first()

        if user:
            return SavedTool.objects.filter(user = user, save_tool = instance).exists()
        else:
            return False
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['feature'] = [feature for feature in data['feature'] if feature]
        data['ratings'] = [rating for rating in data['ratings'] if rating]
        return data
    
    def update(self, instance, validated_data):
        identity = self.context["request"].headers.get("identity")
        user = User.objects.filter(id=identity).first()

        if not user:
            raise serializers.ValidationError({'detail': 'User not found.'})

        save_count = validated_data.get("save_count")

        if save_count is not None:
            if save_count > instance.save_count:
                instance.save_count = save_count
                instance.save()
                saved_tool_obj, _ = SavedTool.objects.get_or_create(
                    save_tool=instance, user=user
                )
            else:
                saved_tool_obj = SavedTool.objects.filter(save_tool=instance, user=user).first()
                instance.save_count = save_count
                instance.save()
                if saved_tool_obj:
                    saved_tool_obj.delete()

        return instance
