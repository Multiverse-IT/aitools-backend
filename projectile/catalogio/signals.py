def update_tool_on_deal_save(sender, instance, **kwargs):
    """
    Signal handler to update connected tool when a deal_tool is saved.
    """
    connected_tool = instance.deal_tool
    connected_tool.discout = instance.discout
    connected_tool.coupon = instance.coupon
    if instance.is_top == True:
        connected_tool.is_deal = True
    if instance.is_top == False:
        connected_tool.is_deal = False
    connected_tool.save()

def delete_deal_tool(sender, instance, **kwargs):
    """
    Signal handler to update connected tools when a deal_tool is deleted.
    """
    connected_tool = instance.deal_tool
    connected_tool.discout = 0
    connected_tool.coupon = ""
    connected_tool.is_deal = False
    connected_tool.save()


def updated_feature_tool_related_values(sender, instance, **kwargs):
    try:
        feature_tool = instance.feature_tool
        feature_tool.is_featured = False
        feature_tool.is_category_featured = False
        feature_tool.save()
        print("deleted feature tool and updated tool values accordingly.")
    except:
        print("feature tool deleted but not updated tool instance values.")
