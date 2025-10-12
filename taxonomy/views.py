from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Skill, Course
from .serializers import SkillSerializer, CourseSerializer

class ReadOnlySet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

class SkillViewSet(ReadOnlySet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    search_fields = ["name", "category"]
    ordering_fields = ["name", "category"]

class CourseViewSet(ReadOnlySet):
    queryset = Course.objects.all().prefetch_related("course_skills__skill")
    serializer_class = CourseSerializer
    search_fields = ["title", "provider", "description"]
    ordering_fields = ["title", "provider", "difficulty", "duration_hours"]
    filterset_fields = ["difficulty", "provider"]
