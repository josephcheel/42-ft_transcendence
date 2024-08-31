from django.contrib.auth.models import AbstractUser
from django.db import models


#
class User(AbstractUser):

    puntos = models.IntegerField(default=10)
    puntos_reservados = models.IntegerField(default=10)
    
    def save_password(self, password):
        self.set_password(password)
        self.save()