from rest_framework import serializers
from .models import Company, Industry

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ("id", "slug", "name")

class CompanySerializer(serializers.ModelSerializer):
    industries = IndustrySerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = (
            "id",
            "name",              # название компании
            "website",           # сайт
            "email_domain",      # домен почты
            "about_text",        # описание
            "is_trusted",        # доверенный
            "status",            # статус модерации (ru-строка приходит через choices)
            "created_at",
            "industries",        # список направлений
        )
