from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Count

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
    average_ratings = serializers.DecimalField(max_digits=3, decimal_places=1, read_only=True)
    is_loved = serializers.SerializerMethodField(read_only=True)
    ratings_distribution = serializers.SerializerMethodField(read_only=True)

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
            "ratings_distribution",
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
    
    # def get_ratings_distribution(self, instance):
    #     # Get the ratings distribution for the given tool instance
    #     ratings_distribution = instance.toolsconnector_set.values('rating__rating').annotate(
    #         count=Count('rating__rating')
    #     ).order_by('rating__rating')
    #     print("rating distribution:", ratings_distribution)

    #     # Create a dictionary to represent the distribution
    #     distribution_dict = {str(Decimal(i)): 0 for i in range(5, 0, -1)}  # Ratings from 1 to 5
    #     for rating_entry in ratings_distribution:
    #         print("rating entry:", rating_entry)
    #         rating_value = str(rating_entry['rating__rating'])
    #         print("rating value:", rating_value)
    #         distribution_dict[rating_value] = rating_entry['count']
    #         print("distribuion dict after adding value:", distribution_dict)

    #     # Calculate percentages
    #     total_ratings = sum(distribution_dict.values())
    #     print("total ratings:", total_ratings)
    #     percentages = {rating_value: (count / total_ratings) * 100 if total_ratings > 0 else 0
    #                    for rating_value, count in distribution_dict.items()}
        
    #     print("percentage:", percentages)
    #     return percentages
    def get_ratings_distribution(self, instance):
        # Get the ratings distribution for the given tool instance
        ratings_distribution = instance.toolsconnector_set.values('rating__rating').annotate(
            count=Count('rating__rating')
        ).order_by('rating__rating')  # Order by rating in ascending order
        
        print("rating distribution:", ratings_distribution)

        # Create a dictionary to represent the distribution
        distribution_dict = {i: 0 for i in range(5, 0, -1)}  # Ratings from 5 to 1
        print("dict or dist:", distribution_dict)

        for rating_entry in ratings_distribution:
            rating_value = rating_entry['rating__rating']
            print("rating value:", rating_value)
            # Round the rating value to the nearest integer and convert to integer
            key = int(round(rating_value))
            print("key:", key)
            # Update existing values
            if key in distribution_dict:
                distribution_dict[key] += rating_entry['count']
                print("dis dict key:", distribution_dict)

        # Calculate percentages
        total_ratings = sum(distribution_dict.values())
        print("total ratings:", total_ratings
              )
        percentages = {str(key): int((count / total_ratings) * 100) if total_ratings > 0 else 0
                       for key, count in distribution_dict.items()}

        return percentages
    

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



class PublicTrendingToolListSerializer(serializers.ModelSerializer):
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
    average_ratings = serializers.DecimalField(max_digits=3, decimal_places=1, read_only=True)
    is_loved = serializers.SerializerMethodField(read_only=True)
    total_saved_tools = serializers.IntegerField(read_only=True, default=0)
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
            "total_saved_tools",
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