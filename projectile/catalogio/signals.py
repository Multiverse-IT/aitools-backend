def update_tool_on_deal_save(sender, instance, **kwargs):
    """
    Signal handler to update connected tool when a deal_tool is saved.
    """
    connected_tool = instance.deal_tool
    connected_tool.discout = instance.discout
    connected_tool.coupon = instance.coupon
    connected_tool.is_deal = True
    connected_tool.save()


def delete_deal_tool(sender, instance, **kwargs):
    """
    Signal handler to update connected tools when a deal_tool is deleted.
    """
    connected_tool = instance.deal_tool
    connected_tool.discout = 0
    connected_tool.coupon = None
    connected_tool.is_deal = False
    connected_tool.save()
