from django.urls import path
from .views import VideoMetaDataView

urlpatterns = [
    path('details/', VideoMetaDataView.as_view(), name="video_details"),
]
