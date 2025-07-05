from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models.user import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("email", "name", "is_staff", "is_active")
    list_filter = ("email", "name", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
