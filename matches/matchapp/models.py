from django.db import models

# Create your models here.


class Invitation(models.Model):
    start_time = models.TimeField()
    player_id = models.ForeignKey("usermodel.User",on_delete=models.CASCADE)