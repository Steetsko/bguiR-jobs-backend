from django.db import models


class Company(models.Model):
    class Category(models.TextChoices):
        TECH = "tech", "Tech / IT"
        ENGINEERING = "engineering", "Engineering"
        MARKETING = "marketing", "Marketing"
        GAMEDEV = "gamedev", "GameDev"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    name = models.CharField(max_length=200, unique=True)
    website = models.URLField(blank=True, default="")
    email_domain = models.CharField(
        max_length=120, blank=True, default="", help_text="example: epam.com"
    )
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.TECH
    )
    about_text = models.TextField(blank=True, default="")
    is_trusted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        return self.name
