from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "website", "email_domain", "category",
                  "about_text", "is_trusted", "status", "created_at")
