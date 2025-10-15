from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "company", "phone", "telegram", "created_at")
    list_filter = ("role", "company")
    search_fields = ("user__username", "user__email", "phone", "telegram")
    autocomplete_fields = ("company",)
