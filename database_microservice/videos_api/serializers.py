from rest_framework import serializers
from .models import VideoMetaData


class VideoMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoMetaData
        fields = '__all__'
