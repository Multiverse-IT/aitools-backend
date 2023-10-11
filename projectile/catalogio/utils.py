
def get_tools_media_path_prefix(instance, filename):
    return f"tools/{instance.slug}/{filename}"

def get_tool_slug(instance):
    return f"{instance.name}"

def get_feature_slug(instance):
    return f"{instance.title}"

def get_category_slug(instance):
    return f"{instance.title}"

def get_sub_category_slug(instance):
    return f"{instance.title}"