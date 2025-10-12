from django.contrib import admin
from .models import Skill, Course, CourseSkill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category")
    list_filter = ("category",)

class CourseSkillInline(admin.TabularInline):
    model = CourseSkill
    extra = 1
    autocomplete_fields = ("skill",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "provider", "difficulty", "duration_hours")
    list_filter = ("provider", "difficulty")
    search_fields = ("title", "provider", "description")
    inlines = [CourseSkillInline]

@admin.register(CourseSkill)
class CourseSkillAdmin(admin.ModelAdmin):
    list_display = ("course", "skill", "coverage_weight")
    list_filter = ("course", "skill")
    autocomplete_fields = ("course", "skill")
