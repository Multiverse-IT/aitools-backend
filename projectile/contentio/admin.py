from django.contrib import admin
from .models import Post, CommonStorage, Redirect

admin.site.register(Post)

admin.site.register(CommonStorage)

admin.site.register(Redirect)