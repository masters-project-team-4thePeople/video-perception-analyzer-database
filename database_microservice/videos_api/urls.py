from django.urls import path
from .views import VideoMetaDataView, VideoDetailsView, VideoSpaceView, DashboardUsersView, DashboardVideosView

urlpatterns = [
    path('details/', VideoMetaDataView.as_view(), name="video_details"),
    path('information/', VideoDetailsView.as_view(), name="video_information"),
    path('spaces/', VideoSpaceView.as_view(), name="video_space_information"),
    path('dashboard_users/', DashboardUsersView.as_view(), name="dashboard_users"),
    path('dashboard_videos/', DashboardVideosView.as_view(), name="dashboard_videos"),
]
