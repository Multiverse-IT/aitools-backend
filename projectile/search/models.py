from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModelWithUID

User = get_user_model()


class Keyword(BaseModelWithUID):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"UID: {self.uid}, Name: {self.name}"


class KeywordSearch(BaseModelWithUID):
    keyword = models.ForeignKey(Keyword, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    search_count = models.PositiveBigIntegerField(default=0)

    def __str__(self)-> str:
        return f"Name: {self.keyword.name}"
