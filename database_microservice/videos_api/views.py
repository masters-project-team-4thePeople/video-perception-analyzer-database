from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import VideoMetaDataSerializer
from .models import VideoMetaData


# Create your views here.
class VideoMetaDataView(APIView):
    def get_video_object(self, video_title):
        try:
            return VideoMetaData.objects.get(username=video_title)
        except Exception as e:
            return None

    def get(self, request):
        video_title = request.data.get('video_title')
        video_instance = self.get_video_object(video_title)

        if not video_instance:
            return Response(
                {
                    "message": "Video with Title Doesn't Exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        video_serializer = VideoMetaDataSerializer(video_instance)
        return Response(video_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VideoMetaDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        video_title = request.data.get('video_title')
        video_instance = self.get_video_object(video_title)

        if not video_instance:
            return Response(
                {
                    "message": "Video with Title Doesn't Exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        video_data = {}

        if request.data.get('video_likes'):
            video_data.update(
                {'video_likes': request.data.get('video_likes')}
            )

        if request.data.get('video_dislikes'):
            video_data.update(
                {'video_dislikes': request.data.get('video_dislikes')}
            )

        if request.data.get('video_transcription'):
            video_data.update(
                {'video_transcription': request.data.get('video_transcription')}
            )

        if request.data.get('video_category'):
            video_data.update(
                {'video_category': request.data.get('video_category')}
            )

        if request.data.get('video_information'):
            video_data.update(
                {'video_information': request.data.get('video_information')}
            )

        video_serializer = VideoMetaDataSerializer(instance=video_instance,
                                                   data=video_data,
                                                   partial=True)

        if video_serializer.is_valid():
            video_serializer.save()
            return Response(video_serializer.data, status=status.HTTP_200_OK)

        return Response(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
