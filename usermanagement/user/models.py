from django.contrib.auth import get_user_model

from django.db import models
try:
    from usermodel.models import User
except:
    pass

User = get_user_model()

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def change_status(self, status):
        self.is_online = status
        self.save()
