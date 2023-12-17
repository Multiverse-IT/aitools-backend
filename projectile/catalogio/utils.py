import random
import string


def get_tools_media_path_prefix(instance, filename):
    return f"tools/{instance.slug}/{filename}"


def get_category_media_path_prefix(instance, filename):
    return f"category/{instance.slug}/{filename}"


def get_subategory_media_path_prefix(instance, filename):
    return f"subcategory/{instance.slug}/{filename}"


def get_feature_slug(instance):
    characters = string.ascii_letters + string.digits
    random_slug = "".join(random.choice(characters) for _ in range(6))
    return random_slug
