from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    class Roles(models.TextChoices):
        STUDENT = "student", "Студент"
        COMPANY = "company", "Представитель компании"
        ADMIN   = "admin",   "Администратор"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    role = models.CharField(
        "Роль",
        max_length=20,
        choices=Roles.choices,
        default=Roles.STUDENT,
    )
    # связь с компаниями (если представитель компании)
    # можно убрать/добавить по необходимости
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Компания",
    )
    phone = models.CharField("Телефон", max_length=32, blank=True)
    telegram = models.CharField("Telegram", max_length=64, blank=True)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
