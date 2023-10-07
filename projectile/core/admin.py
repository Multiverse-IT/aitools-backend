from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "email",
        "first_name",
        "last_name",
        "slug",
        "phone",
        "is_active",
        "status",
        "gender",
        "date_joined",
        "last_login",
    ]
    list_filter = UserAdmin.list_filter + ("status",)
    ordering = ("-date_joined",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Extra Fields",
            {
                "fields": (
                    "phone",
                    "image",
                    "gender",
                    "status",
                    "date_of_birth",
                )
            },
        ),
    )
