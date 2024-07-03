from rest_framework import serializers

from catalogio.models import Category, SubCategory, ToolsCategoryConnector
from common.serializers import CategorySlimSerializer, SubCategorySlimSerializer
from contentio.models import FAQ, FaqCategoryConnector
from contentio.rest.serializers.faq import GlobalFaqListSerializer, GlobalFaqListSlimSerializer

class SubCategoriesSlimSerializer(serializers.ModelSerializer):
    total_tools = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SubCategory
        fields = ("title","slug", "total_tools")

    def get_total_tools(self, obj):
        return obj.toolscategoryconnector_set.filter(tool__isnull=False).count()


class CatetoryListSerializer(serializers.ModelSerializer):
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "slug",
            "title",
            "subcategory",
            "meta_title",
            "meta_description",
            "image",
            "alt",
            "is_indexed",
            "canonical_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]

    def get_subcategory(self, obj):
        subcategories_ids = (
            obj.toolscategoryconnector_set.select_related("subcategory")
            .filter()
            .values_list("subcategory_id", flat=True)
        ).distinct()
        subcategories = SubCategory.objects.filter(id__in=subcategories_ids).distinct()
        return SubCategoriesSlimSerializer(subcategories, many=True).data


class SubCatetoryListDetailSerializer(serializers.ModelSerializer):
    category_slug = serializers.SlugRelatedField(
        "slug", queryset=Category.objects.filter(), write_only=True, required=True
    )
    category = CategorySlimSerializer(
        source="toolscategoryconnector_set.first", read_only=True
    )
    faq_uids = serializers.ListField(
        write_only=True, required=False, child=serializers.CharField()
    )

    faqs = GlobalFaqListSlimSerializer(
        source="faqcategoryconnector_set", many=True, read_only=True
    )
    class Meta:
        model = SubCategory
        fields = [
            "slug",
            "title",
            "description",
            "category_slug",
            "category",
            "meta_title",
            "meta_description",
            "image",
            "alt",
            "faq_uids",
            "faqs",
            "is_noindex",
            "focus_keyword",
            "canonical_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "uid",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        category = validated_data.pop("category_slug", None)
        faq_uids = validated_data.pop("faq_uids", None)

        sub_category = SubCategory.objects.create(**validated_data)
        category_connector, _ = ToolsCategoryConnector.objects.get_or_create(
            category=category, subcategory=sub_category
        )
        if faq_uids:
            faqs = FAQ.objects.filter(uid__in=faq_uids)
            try:
                connectors = [
                    FaqCategoryConnector(
                        faq=faq,
                        sub_category=sub_category,
                    )
                    for faq in faqs
                ]
                FaqCategoryConnector.objects.bulk_create(connectors)

            except Exception as e:
                print("detail:", e)

        return sub_category

    def update(self, instance, validated_data):
        faq_uids = validated_data.pop("faq_uids", None)

        if category := validated_data.pop("category_slug", None):
            category_connector = ToolsCategoryConnector.objects.filter(
                subcategory=instance
            ).first()
            category_connector.category = category
            category_connector.save()

        if faq_uids:
            instance.faqcategoryconnector_set.all().delete()
            faqs = FAQ.objects.filter(uid__in=faq_uids)
            try:
                connectors = [
                    FaqCategoryConnector(
                        faq=faq,
                        sub_category=instance,
                    )
                    for faq in faqs
                ]
                FaqCategoryConnector.objects.bulk_create(connectors)

            except Exception as e:
                print("detail:", e)

        return super().update(instance, validated_data)
