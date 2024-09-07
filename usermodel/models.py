from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    puntos = models.IntegerField(default=10)
    puntos_reservados = models.IntegerField(default=10)
    original_username =  models.CharField(max_length=100)
    tournament_name = models.CharField(max_length=100)
    
    def update_fields(self, **kwargs):
        for field in kwargs:
            if field in ['first_name', 'last_name', 'tournament_name'] and hasattr(self, field):
                setattr(self, field, kwargs[field])
        self.save()