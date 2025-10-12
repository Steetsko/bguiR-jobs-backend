from django.db import models
from django.utils.translation import gettext_lazy as _


class Industry(models.Model):
    slug = models.SlugField(_("слаг"), max_length=50, unique=True,
                            help_text=_("Короткий код латиницей — например backend, devops"))
    name = models.CharField(_("название"), max_length=120, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Направление (категория)")
        verbose_name_plural = _("Направления (категории)")

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("На модерации")
        APPROVED = "approved", _("Одобрена")
        REJECTED = "rejected", _("Отклонена")

    name = models.CharField(_("название компании"), max_length=200, unique=True)
    website = models.URLField(_("сайт"), blank=True, default="")
    email_domain = models.CharField(
        _("домен почты"),
        max_length=120,
        blank=True,
        default="",
        help_text=_("Напр.: epam.com — пригодится для быстрой верификации"),
    )
    about_text = models.TextField(_("о компании"), blank=True, default="")
    is_trusted = models.BooleanField(_("доверенный работодатель"), default=False)

    status = models.CharField(
        _("статус модерации"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text=_("Управляет публикацией вакансий: одобрена/на модерации/отклонена"),
    )

    # 🔽 мультивыбор направлений
    industries = models.ManyToManyField(
        Industry,
        verbose_name=_("направления (категории)"),
        blank=True,
        related_name="companies",
        help_text=_("Выберите одно или несколько направлений деятельности"),
    )

    created_at = models.DateTimeField(_("создано"), auto_now_add=True)
    updated_at = models.DateTimeField(_("обновлено"), auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["status"])]
        verbose_name = _("Компания")
        verbose_name_plural = _("Компании")

    def __str__(self) -> str:
        return self.name
