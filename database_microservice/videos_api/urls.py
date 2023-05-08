from django.urls import path
from .views import VideoMetaDataView, VideoDetailsView, VideoSpaceView

urlpatterns = [
    path('details/', VideoMetaDataView.as_view(), name="video_details"),
    path('information/', VideoDetailsView.as_view(), name="video_information"),
    path('spaces/', VideoSpaceView.as_view(), name="video_space_information"),
]
