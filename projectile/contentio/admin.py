from django.contrib import admin
from .models import Post, CommonStorage, Redirect, Sponsor, FAQ, FaqCategoryConnector

admin.site.register(Post)

admin.site.register(CommonStorage)

admin.site.register(Redirect)

admin.site.register(Sponsor)

admin.site.register(FAQ)

admin.site.register(FaqCategoryConnector)