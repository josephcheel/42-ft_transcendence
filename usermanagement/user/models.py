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

class Friendship(models.Model):
    users = models.ManyToManyField(User)
    DECLINED_CHOIDE = 0
    ACCEPTED_CHOICE = 1
    PENDING_CHOICE = 2


    STATUS_CHOICES = [
        {ACCEPTED_CHOICE, "accepted"},
        {PENDING_CHOICE, "pending"},
        {DECLINED_CHOIDE, "declined"},
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING_CHOICE)

    @staticmethod
    def add_friendship(user1, user2):
        friends = Friendship()
        friends.save()
        friends.users.add(user1, user2)

    @staticmethod
    def remove_friendship(user1, user2):
        friendship = Friendship.objects.filter(users=user1).filter(users=user2).first()
        if friendship:
            friendship.delete()
    
    @staticmethod
    def are_friends(user1, user2):
        return Friendship.objects.filter(users=user1).filter(users=user2).exists()

    

