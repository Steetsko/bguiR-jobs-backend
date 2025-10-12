from django.db import models
from django.utils.translation import gettext_lazy as _

class Skill(models.Model):
    name = models.CharField(_("название"), max_length=120, unique=True)
    category = models.CharField(_("категория"), max_length=120, blank=True, default="")
    description = models.TextField(_("описание"), blank=True, default="")

    class Meta:
        ordering = ["name"]
        verbose_name = _("Навык")
        verbose_name_plural = _("Навыки")

    def __str__(self):
        return self.name


class Course(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = "beginner", _("Начинающий")
        INTERMEDIATE = "intermediate", _("Средний")
        ADVANCED = "advanced", _("Продвинутый")

    title = models.CharField(_("название"), max_length=200)
    description = models.TextField(_("описание"), blank=True, default="")
    provider = models.CharField(_("провайдер"), max_length=120, blank=True, default="")
    duration_hours = models.PositiveIntegerField(_("длительность (часы)"), default=0)
    difficulty = models.CharField(
        _("сложность"),
        max_length=20, 
        choices=Difficulty.choices, 
        default=Difficulty.BEGINNER
    )

    class Meta:
        ordering = ["title"]
        verbose_name = _("Курс")
        verbose_name_plural = _("Курсы")

    def __str__(self):
        return self.title


class CourseSkill(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name="course_skills",
        verbose_name=_("курс")
    )
    skill = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE, 
        related_name="skill_courses",
        verbose_name=_("навык")
    )
    coverage_weight = models.DecimalField(
        _("вес покрытия"), 
        max_digits=3, 
        decimal_places=2, 
        default=1.00
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["course", "skill"], name="uq_course_skill"),
        ]
        verbose_name = _("Навык курса")
        verbose_name_plural = _("Навыки курсов")

    def __str__(self):
        return f"{self.course} → {self.skill} ({self.coverage_weight})"
