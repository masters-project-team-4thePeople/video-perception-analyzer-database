from django.db import models
from users_api.models import UserProfile


# Create your models here.
class VideoMetaData(models.Model):
    video_id = models.BigAutoField(primary_key=True)
    video_url = models.CharField(max_length=512, unique=True)
    video_title = models.CharField(max_length=256, default='', blank=True, null=True)
    video_duration = models.FloatField(default=0.0, blank=True, null=True)
    video_likes = models.IntegerField(default=0, blank=True, null=True)
    video_dislikes = models.IntegerField(default=0, blank=True, null=True)
    video_transcription = models.CharField(max_length=2048, default='', blank=True, null=True)
    video_category = models.JSONField(blank=True, null=True)
    video_information = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.video_id)


class VideoDetails(models.Model):
    current_processing_status = (
        ("INITIALIZED", "INITIALIZED"),
        ("STARTED", "STARTED"),
        ("QUEUED", "QUEUED"),
        ("COMPLETED", "COMPLETED"),
        ("ABORTED", "ABORTED")
    )

    current_status = (
        ("QUEUED", "QUEUED"),
        ("ACCEPTED", "ACCEPTED"),
        ("REJECTED", "REJECTED")
    )

    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    video_id = models.OneToOneField(VideoMetaData, on_delete=models.CASCADE, blank=True, null=True)
    vpa_pipeline_status = models.CharField(max_length=36, choices=current_processing_status,
                                           default="INITIALIZED", blank=True, null=True)

    vpa_video_status = models.CharField(max_length=36, choices=current_status,
                                        default="QUEUED", blank=True, null=True)

    def __str__(self):
        return str(self.video_id)


class UploadedVideos(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField()
    username = models.CharField(max_length=64, default="", blank=True, null=True)
    video_file_url = models.CharField(max_length=2048, default="", blank=True, null=True)
