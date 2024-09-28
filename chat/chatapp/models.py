from django.db import models
from django.conf import settings  # Dynamically references the User model

# Create your models here.
class Chatsession(models.Model):
    pass

class Chat(models.Model):
    session = models.ForeignKey(Chatsession, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat.user')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)