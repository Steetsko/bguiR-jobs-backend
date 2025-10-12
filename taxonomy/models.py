from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=120, blank=True, default="")
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    provider = models.CharField(max_length=120, blank=True, default="")
    duration_hours = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(
        max_length=20, choices=Difficulty.choices, default=Difficulty.BEGINNER
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class CourseSkill(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="skill_courses")
    coverage_weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["course", "skill"], name="uq_course_skill"),
        ]

    def __str__(self):
        return f"{self.course} → {self.skill} ({self.coverage_weight})"
