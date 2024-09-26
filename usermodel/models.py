from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    original_username =  models.CharField(max_length=100, null=True)
    tournament_name = models.CharField(max_length=100, null = True)
    puntos = models.IntegerField(default=1000)
    puntos_reservados = models.IntegerField(default=0)
    # Specify a unique related_name for the groups field
    groups = models.ManyToManyField(
        'auth.Group', related_name='users_db_Group', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='users_db_Permission', blank=True)
    def update_fields(self, **kwargs):
        for field in kwargs:
            if field in ['first_name', 'last_name', 'tournament_name'] and hasattr(self, field):
                setattr(self, field, kwargs[field])
        self.save()