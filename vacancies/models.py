from django.db import models
from django.utils.translation import gettext_lazy as _
from companies.models import Company
from taxonomy.models import Skill


class Vacancy(models.Model):
    class Grade(models.TextChoices):
        INTERN = "intern", _("Стажер")
        JUNIOR = "junior", _("Джуниор")
        MIDDLE = "middle", _("Мидл")
        SENIOR = "senior", _("Сеньор")

    class Employment(models.TextChoices):
        FULLTIME = "fulltime", _("Полная занятость")
        PARTTIME = "parttime", _("Частичная занятость")
        INTERN = "internship", _("Стажировка")
        CONTRACT = "contract", _("Контракт")

    class Status(models.TextChoices):
        DRAFT = "draft", _("Черновик")
        MODERATION = "moderation", _("На модерации")
        PUBLISHED = "published", _("Опубликована")
        ARCHIVED = "archived", _("Архивная")

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name="vacancies",
        verbose_name=_("компания")
    )
    title = models.CharField(_("название"), max_length=200)
    description_md = models.TextField(_("описание"))  # Markdown/текст описания
    grade = models.CharField(
        _("уровень"),
        max_length=12, 
        choices=Grade.choices, 
        default=Grade.JUNIOR
    )
    employment_type = models.CharField(
        _("тип занятости"),
        max_length=12, 
        choices=Employment.choices, 
        default=Employment.FULLTIME
    )
    location = models.CharField(_("локация"), max_length=120, blank=True, default="")
    is_remote = models.BooleanField(_("удаленная работа"), default=True)
    salary_min = models.PositiveIntegerField(_("мин. зарплата"), null=True, blank=True)
    salary_max = models.PositiveIntegerField(_("макс. зарплата"), null=True, blank=True)
    status = models.CharField(
        _("статус"),
        max_length=12, 
        choices=Status.choices, 
        default=Status.MODERATION
    )

    created_at = models.DateTimeField(_("создано"), auto_now_add=True)
    updated_at = models.DateTimeField(_("обновлено"), auto_now=True)

    skills = models.ManyToManyField(
        Skill, 
        through="VacancySkill", 
        related_name="vacancies",
        verbose_name=_("навыки")
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["grade"]),
            models.Index(fields=["employment_type"]),
        ]
        verbose_name = _("Вакансия")
        verbose_name_plural = _("Вакансии")

    def __str__(self) -> str:
        return f"{self.title} @ {self.company.name}"


class VacancySkill(models.Model):
    class Weight(models.IntegerChoices):
        NICE_TO_HAVE = 1, _("Желательно")
        REQUIRED = 2, _("Обязательно")

    vacancy = models.ForeignKey(
        Vacancy, 
        on_delete=models.CASCADE, 
        related_name="vacancy_skills",
        verbose_name=_("вакансия")
    )
    skill = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE, 
        related_name="skill_vacancies",
        verbose_name=_("навык")
    )
    weight = models.IntegerField(
        _("важность"), 
        choices=Weight.choices, 
        default=Weight.REQUIRED
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vacancy", "skill"], name="uq_vacancy_skill"
            )
        ]
        verbose_name = _("Навык вакансии")
        verbose_name_plural = _("Навыки вакансий")

    def __str__(self) -> str:
        return f"{self.vacancy} → {self.skill} ({self.get_weight_display()})"
