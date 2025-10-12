from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Vacancy, VacancySkill


class VacancySkillInline(admin.TabularInline):
    model = VacancySkill
    extra = 1
    autocomplete_fields = ("skill",)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "grade",
        "employment_type",
        "is_remote",
        "status",
        "created_at",
    )
    list_filter = ("company", "grade", "employment_type", "status", "is_remote")
    search_fields = ("title", "description_md", "company__name", "location")
    readonly_fields = ("created_at", "updated_at")
    inlines = [VacancySkillInline]
    
    fieldsets = (
        (None, {"fields": ("title", "company", "description_md")}),
        (_("Условия работы"), {"fields": ("grade", "employment_type", "location", "is_remote")}),
        (_("Зарплата"), {"fields": ("salary_min", "salary_max")}),
        (_("Статус"), {"fields": ("status",)}),
        (_("Служебное"), {"fields": ("created_at", "updated_at")}),
    )


@admin.register(VacancySkill)
class VacancySkillAdmin(admin.ModelAdmin):
    list_display = ("vacancy", "skill", "weight")
    list_filter = ("weight", "skill", "vacancy__company")
    autocomplete_fields = ("vacancy", "skill")
