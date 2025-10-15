from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created, **kwargs):
    """
    Автоматически создаём профиль сразу после создания User.
    """
    if created:
        UserProfile.objects.create(user=instance)
