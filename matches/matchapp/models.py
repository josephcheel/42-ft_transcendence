from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Invitation(models.Model):
    DECLINED_CHOIDE = 0
    ACCEPTED_CHOICE = 1
    PENDING_CHOICE = 2


    STATUS_CHOICES = [
        {ACCEPTED_CHOICE, "accepted"},
        {PENDING_CHOICE, "pending"},
        {DECLINED_CHOIDE, "declined"},
    ]
    creation_time = models.DateTimeField(blank=False, null=False)
    start_time = models.DateTimeField(blank=False, null=False)
    player_id = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING_CHOICE)
    owner= models.BooleanField(default=False)