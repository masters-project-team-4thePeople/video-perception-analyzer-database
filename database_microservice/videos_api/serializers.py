from rest_framework import serializers
from .models import VideoMetaData, VideoDetails


class VideoMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoMetaData
        fields = '__all__'


class VideoDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoDetails
        fields = '__all__'
