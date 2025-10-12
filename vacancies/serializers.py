from rest_framework import serializers
from .models import Vacancy, VacancySkill
from taxonomy.serializers import SkillSerializer  # если нет — см. ранее
from companies.serializers import CompanySerializer

class VacancySkillReadSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    class Meta:
        model = VacancySkill
        fields = ("skill", "weight")

class VacancySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    vacancy_skills = VacancySkillReadSerializer(many=True, read_only=True)

    class Meta:
        model = Vacancy
        fields = ("id", "title", "description_md", "company", "grade",
                  "employment_type", "location", "is_remote",
                  "salary_min", "salary_max", "status",
                  "created_at", "vacancy_skills")
