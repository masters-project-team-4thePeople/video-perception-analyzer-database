from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserPreference


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'birth_date',
                  'notification_id']


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference