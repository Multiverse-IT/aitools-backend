
from celery import shared_task

from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

from .models import Tool

@shared_task
def update_new_tool_status():
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    past_tools = Tool.objects.filter(
        is_new=True,
        created_at__lte=twenty_four_hours_ago
    ).update(is_new=False)
    logger.info(f"{past_tools} tools updated. Time: {timezone.now()}")
