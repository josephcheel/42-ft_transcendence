from django.db import models
from django.conf import settings  # Dynamically references the User model

# Create your models here.
class Chatsession(models.Model):
    user_1 = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='user_1_sessions',
    on_delete=models.CASCADE
    )