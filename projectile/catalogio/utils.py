
def get_tools_media_path_prefix(instance, filename):
    return f"tools/{instance.slug}/{filename}"

def get_category_media_path_prefix(instance, filename):
    return f"category/{instance.slug}/{filename}"


def get_subategory_media_path_prefix(instance, filename):
    return f"subcategory/{instance.slug}/{filename}"