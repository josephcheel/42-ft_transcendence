from django.contrib.auth import get_user_model 
from django.db import models
from django.conf import settings

#if settings.DEBUG:
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    original_username = models.CharField(max_length=100, null=True)
    tournament_name = models.CharField(max_length=100, null=True)
    puntos = models.IntegerField(default=1000)
    puntos_reservados = models.IntegerField(default=0)
    ethereum_address = models.CharField(max_length=44, null=True)
    ethereum_private_key = models.CharField(max_length=66, null=True, blank=True)
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

    def get_all(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'username': self.original_username, "tournament_name": self.tournament_name, 'is_online': self.userstatus.is_online, 'profile_picture_url': self.userprofilepic.picture.url}



User = get_user_model()

class UserStatus(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

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
