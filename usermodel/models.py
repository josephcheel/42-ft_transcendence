from django.contrib.auth.models import AbstractUser
from django.db import models

#
class User(AbstractUser):
    original_username =  models.CharField(max_length=100)
