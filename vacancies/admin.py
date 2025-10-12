from django.contrib import admin
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


@admin.register(VacancySkill)
class VacancySkillAdmin(admin.ModelAdmin):
    list_display = ("vacancy", "skill", "weight")
    list_filter = ("weight", "skill", "vacancy__company")
    autocomplete_fields = ("vacancy", "skill")
