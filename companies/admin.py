from django.contrib import admin
from .models import Company, Industry


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_trusted", "status", "website")
    list_filter = ("status", "is_trusted", "industries")
    search_fields = ("name", "website", "email_domain", "about_text")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("industries",)

    fieldsets = (
        (None, {"fields": ("name", "website", "email_domain", "about_text")}),
        ("Публикация", {"fields": ("status", "is_trusted")}),
        ("Категории", {"fields": ("industries",)}),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )
