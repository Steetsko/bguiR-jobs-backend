from rest_framework import serializers
from .models import Skill, Course, CourseSkill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("id", "name", "category", "description")

class CourseSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    class Meta:
        model = CourseSkill
        fields = ("skill", "coverage_weight")

class CourseSerializer(serializers.ModelSerializer):
    course_skills = CourseSkillSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ("id", "title", "description", "provider",
                  "duration_hours", "difficulty", "course_skills")
