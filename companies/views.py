from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Company.objects.all().order_by("name")
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "status", "is_trusted"]
    search_fields = ["name", "website", "email_domain", "about_text"]
    ordering_fields = ["name", "created_at"]
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company
from .serializers import CompanySerializer

class CompanyFilter(FilterSet):
    industry = CharFilter(method="filter_industry")  # ?industry=backend или ?industry=3

    def filter_industry(self, qs, name, value):
        if value.isdigit():
            return qs.filter(industries__id=int(value))
        return qs.filter(industries__slug=value)

    class Meta:
        model = Company
        fields = ["status", "is_trusted"]

class CompanyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Company.objects.prefetch_related("industries").all().order_by("name")
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CompanyFilter
    search_fields = ["name", "website", "email_domain", "about_text", "industries__name"]
    ordering_fields = ["name", "created_at"]
