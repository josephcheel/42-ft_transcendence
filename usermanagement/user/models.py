from django.contrib.auth import get_user_model 
from django.db import models
from django.conf import settings

if settings.DEBUG:
    from django.contrib.auth.models import AbstractUser
    class User(AbstractUser):
        original_username =  models.CharField(max_length=100)

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def change_status(self, status):
        self.is_online = status
        self.save()

class Friendship(models.Model):
    DECLINED_CHOICE = 0
    ACCEPTED_CHOICE = 1
    PENDING_CHOICE = 2
    STATUS_CHOICES = [
        (DECLINED_CHOICE, "declined"),
        (ACCEPTED_CHOICE, "accepted"),
        (PENDING_CHOICE, "pending"),

    ]
    STATUS_DICT = {v: k for k, v in STATUS_CHOICES}
    STATUS_STRING = {v: k for k, v in STATUS_CHOICES}

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=PENDING_CHOICE)
    users = models.ManyToManyField(User)

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
        return Friendship.objects.filter(users=user1).filter(users=user2).exclude(status=Friendship.DECLINED_CHOICE).exists()
    
    @staticmethod
    def get_friendship(user1, user2):
        return Friendship.objects.filter(users=user1).filter(users=user2)
    
    @staticmethod
    def get_friends(user):
        friendships =Friendship.objects.filter(users=user) 
        friends_list = []
        for friendship in friendships:
            friend = friendship.users.exclude(id=user.id).first()
            if friend:
                friends_list.append({
                    'username': friend.original_username,
                    'friendship': friendship.get_status_display(),
                    'is_online' : friend.userstatus.is_online

                }) 
        return friends_list
    
    @classmethod
    def get_status_choice(cls, status_string):
        return cls.STATUS_DICT.get(status_string) 
