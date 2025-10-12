from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_trusted", "status", "website")
    list_filter = ("category", "is_trusted", "status")
    search_fields = ("name", "website", "email_domain")
    readonly_fields = ("created_at", "updated_at")
