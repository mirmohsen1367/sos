from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from profiles.models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    list_display = [
        "id",
        "username",
    ]
    search_fields = ("username",)
    list_display_links = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)
