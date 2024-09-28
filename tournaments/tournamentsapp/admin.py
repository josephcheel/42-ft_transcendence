from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings

if not settings.DEBUG:
	from usermanagement.user.models import User
else:
	from tournamentsapp.models import User
# Register your models here.

admin.site.register(User, UserAdmin)
