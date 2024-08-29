from django.contrib.auth.models import AbstractUser
from django.db import models


#
class User(AbstractUser):
    def save_password(self, password):
        self.set_password(password)
        self.save()