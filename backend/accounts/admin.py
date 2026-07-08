from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin configuration for Role."""

    list_display = ("id", "role_name")

    search_fields = ("role_name",)

    ordering = ("role_name",)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for User."""

    list_display = (
        "username",
        "first_name",
        "email",
        "phone_number",
        "role",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "first_name",
        "email",
    )

    ordering = ("username",)