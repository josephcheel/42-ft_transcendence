from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .metrics import user_created_counter, user_logged_in_counter
from .models import UserProfilePic, UserStatus

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_status(sender, instance, created, **kwargs):
    if created:
        UserStatus.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfilePic.objects.create(user=instance)

@receiver(post_save, sender=User)
def increment_user_created(sender, instance, created, **kwargs):
    if created:
        # Increment the counter when a new user is successfully created
        user_created_counter.inc()

@receiver(user_logged_in)
def increment_user_logged_in(sender, request, user, **kwargs):
    user_logged_in_counter.inc()

@receiver(user_logged_out)
def decrement_user_logged_in(sender, request, user, **kwargs):
    user_logged_in_counter.dec()