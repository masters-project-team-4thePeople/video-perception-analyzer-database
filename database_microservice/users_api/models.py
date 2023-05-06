from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    notification_id = models.CharField(max_length=256, blank=True)


class UserPreference(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    user_categories = models.JSONField(blank=True, null=True)
    user_video_history = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.user_id)
