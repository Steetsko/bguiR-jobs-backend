from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, NumberFilter
from .models import Vacancy
from .serializers import VacancySerializer

class VacancyFilter(FilterSet):
    company = NumberFilter(field_name="company_id")
    skill = CharFilter(method="filter_skill")   # принимает id или имя
    status = CharFilter(field_name="status")
    grade = CharFilter(field_name="grade")

    def filter_skill(self, qs, name, value):
        if value.isdigit():
            return qs.filter(vacancy_skills__skill_id=int(value))
        return qs.filter(vacancy_skills__skill__name__iexact=value)

    class Meta:
        model = Vacancy
        fields = ["company", "skill", "status", "grade", "employment_type", "is_remote"]

class VacancyViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Vacancy.objects.select_related("company")\
        .prefetch_related("vacancy_skills__skill").all()
    serializer_class = VacancySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VacancyFilter
    search_fields = ["title", "description_md", "company__name", "location"]
    ordering_fields = ["created_at", "salary_min", "salary_max"]
    ordering = ["-created_at"]
