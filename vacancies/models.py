from django.db import models
from companies.models import Company
from taxonomy.models import Skill


class Vacancy(models.Model):
    class Grade(models.TextChoices):
        INTERN = "intern", "Intern"
        JUNIOR = "junior", "Junior"
        MIDDLE = "middle", "Middle"
        SENIOR = "senior", "Senior"

    class Employment(models.TextChoices):
        FULLTIME = "fulltime", "Full-time"
        PARTTIME = "parttime", "Part-time"
        INTERN = "internship", "Internship"
        CONTRACT = "contract", "Contract"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        MODERATION = "moderation", "On moderation"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="vacancies"
    )
    title = models.CharField(max_length=200)
    description_md = models.TextField()  # Markdown/текст описания
    grade = models.CharField(
        max_length=12, choices=Grade.choices, default=Grade.JUNIOR
    )
    employment_type = models.CharField(
        max_length=12, choices=Employment.choices, default=Employment.FULLTIME
    )
    location = models.CharField(max_length=120, blank=True, default="")
    is_remote = models.BooleanField(default=True)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.MODERATION
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    skills = models.ManyToManyField(
        Skill, through="VacancySkill", related_name="vacancies"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["grade"]),
            models.Index(fields=["employment_type"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} @ {self.company.name}"


class VacancySkill(models.Model):
    class Weight(models.IntegerChoices):
        NICE_TO_HAVE = 1, "Nice-to-have"
        REQUIRED = 2, "Required"

    vacancy = models.ForeignKey(
        Vacancy, on_delete=models.CASCADE, related_name="vacancy_skills"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name="skill_vacancies"
    )
    weight = models.IntegerField(choices=Weight.choices, default=Weight.REQUIRED)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vacancy", "skill"], name="uq_vacancy_skill"
            )
        ]

    def __str__(self) -> str:
        return f"{self.vacancy} → {self.skill} ({self.get_weight_display()})"
