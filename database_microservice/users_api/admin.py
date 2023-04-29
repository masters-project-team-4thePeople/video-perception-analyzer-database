from django.contrib import admin
from .models import UserProfile, UserPreference

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserPreference)

