from django.contrib import admin
from .models import VideoMetaData, VideoDetails, UploadedVideos

# Register your models here.
admin.site.register(VideoMetaData)
admin.site.register(VideoDetails)
admin.site.register(UploadedVideos)

