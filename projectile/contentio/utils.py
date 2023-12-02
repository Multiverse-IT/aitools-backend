
def get_post_slug(instance):
    return f"{(instance.title)[:6]}"


def get_post_media_path_prefix(instance, filename):
    return f"post/{instance.slug}/filename"
