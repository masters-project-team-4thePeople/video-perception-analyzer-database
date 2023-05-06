from django.urls import path
from .views import UserView, UserPreferenceView

urlpatterns = [
    path('profile/', UserView.as_view(), name="user_profile_views"),
    path('preferences/', UserPreferenceView.as_view(), name="user_preference_views"),
]
