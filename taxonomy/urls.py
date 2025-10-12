from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, CourseViewSet

router = DefaultRouter()
router.register(r"skills", SkillViewSet, basename="skills")
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [path("", include(router.urls))]
