from django.db import models
from users_api.models import UserProfile


# Create your models here.
class VideoMetaData(models.Model):
    video_id = models.BigAutoField(primary_key=True)
    video_url = models.CharField(max_length=512, default='', blank=True, null=True)
    video_title = models.CharField(max_length=256, unique=True)
    video_duration = models.FloatField(default=0.0, blank=True, null=True)
    video_likes = models.IntegerField(default=0, blank=True, null=True)
    video_dislikes = models.IntegerField(default=0, blank=True, null=True)
    video_transcription = models.CharField(max_length=2048, default='', blank=True, null=True)
    video_category = models.JSONField(blank=True, null=True)
    video_information = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.video_id)


class VideoDetails(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    video_id = models.ForeignKey(VideoMetaData, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.video_id)
