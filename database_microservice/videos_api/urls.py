from django.urls import path
from .views import VideoMetaDataView, VideoDetailsView

urlpatterns = [
    path('details/', VideoMetaDataView.as_view(), name="video_details"),
    path('information/', VideoDetailsView.as_view(), name="video_information"),
]
