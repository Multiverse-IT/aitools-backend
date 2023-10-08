
def get_tools_media_path_prefix(instance, filename):
    return f"tools/{instance.slug}/{filename}"

def get_tool_slug(instance):
    return f"{instance.name}"