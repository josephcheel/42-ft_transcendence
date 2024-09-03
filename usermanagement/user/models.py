from django.contrib.auth import get_user_model 
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    original_username =  models.CharField(max_length=100)
    def save_password(self, password):
        self.set_password(password)
        self.save()

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def change_status(self, status):
        self.is_online = status
        self.save()
