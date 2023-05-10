import glob
import logging
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import VideoMetaDataSerializer, VideoDetailsSerializer
from .models import VideoMetaData, VideoDetails, UploadedVideos
from users_api.models import UserProfile, UserPreference
import yaml
from django.core.files.storage import FileSystemStorage


# Create your views here.
class VideoMetaDataView(APIView):
    def get_video_object(self, video_url):
        try:
            return VideoMetaData.objects.get(video_url=video_url)
        except Exception as e:
            return None

    def get(self, request):
        video_url = request.GET.get('video_url')
        video_instance = self.get_video_object(video_url)

        if not video_instance:
            return Response(
                {
                    "message": "Video URL Doesn't Exist"
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
        video_url = request.data.get('video_url')
        video_instance = self.get_video_object(video_url)

        if not video_instance:
            return Response(
                {
                    "message": "Video URL Doesn't Exist"
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


class VideoDetailsView(APIView):
    def get_user_objects(self, user_id):
        try:
            return VideoDetails.objects.filter(user_id=user_id)
        except Exception as e:
            return None

    def get_video_objects(self, video_id):
        try:
            return VideoDetails.objects.get(video_id=video_id)
        except Exception as e:
            return None

    def get_video_details_instance(self, video_id):
        try:
            return VideoMetaData.objects.filter(video_id=video_id)
        except Exception as e:
            return None

    def get_video_details(self, video_id):
        video_instance = self.get_video_details_instance(video_id)
        video_serializer = VideoMetaDataSerializer(video_instance)
        return video_serializer.data

    def get(self, request):
        user_id = request.GET.get('user_id')
        user_instance = self.get_user_objects(user_id)

        if not user_instance:
            return Response(
                {
                    "message": "videos for this user doesn't exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        videos_details = {}
        for videos in user_instance:
            current_video = VideoMetaData.objects.filter(video_id=str(videos.video_id))
            videos_details[str(videos.video_id)] = {}
            if current_video:
                videos_details[str(videos.video_id)].update({
                    'video_url': current_video[0].video_url,
                })

                videos_details[str(videos.video_id)].update({
                    'video_title': current_video[0].video_title,
                })

                videos_details[str(videos.video_id)].update({
                    'video_duration': current_video[0].video_duration,
                })

                videos_details[str(videos.video_id)].update({
                    'video_likes': current_video[0].video_likes,
                })

                videos_details[str(videos.video_id)].update({
                    'video_dislikes': current_video[0].video_dislikes,
                })

                videos_details[str(videos.video_id)].update({
                    'video_transcription': current_video[0].video_transcription,
                })

                videos_details[str(videos.video_id)].update({
                    'video_category': current_video[0].video_category,
                })

                videos_details[str(videos.video_id)].update({
                    'video_information': current_video[0].video_information,
                })

            videos_details[str(videos.video_id)].update({"vpa_pipeline_status": videos.vpa_pipeline_status})
            videos_details[str(videos.video_id)].update({"vpa_video_status": videos.vpa_video_status})

        return Response(videos_details, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VideoDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        video_id = request.data.get('video_id')
        video_instance = self.get_video_objects(video_id)

        if not video_instance:
            return Response(
                {
                    "message": "Video Doesn't Exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        video_data = {}
        if request.data.get('vpa_pipeline_status'):
            video_data.update(
                {'vpa_pipeline_status': request.data.get('vpa_pipeline_status')}
            )

        if request.data.get('vpa_video_status'):
            video_data.update(
                {'vpa_video_status': request.data.get('vpa_video_status')}
            )

        video_serializer = VideoDetailsSerializer(instance=video_instance,
                                                  data=video_data,
                                                  partial=True)

        if video_serializer.is_valid():
            video_serializer.save()
            return Response(video_serializer.data, status=status.HTTP_200_OK)

        return Response(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoSpaceView(APIView):
    def get(self, request):
        all_video_categories = [
            "film_and_animation",
            "autos_and_vehicles",
            "music",
            "pets_and_animals",
            "sports",
            "travel_and_events",
            "gaming",
            "people_and_blogs",
            "comedy",
            "entertainment",
            "news_and_politics",
            "how_to_and_style",
            "education",
            "science_and_technology",
            "nonprofits_and_activism"
        ]

        all_video_objects = UploadedVideos.objects.filter(username__in=all_video_categories)
        all_video_details = {}

        for category in all_video_categories:
            all_video_details[category] = []

        for videos in all_video_objects:
            all_video_details[videos.username].append(videos.video_file_url)

        return Response(all_video_details, status=status.HTTP_200_OK)

    def post(self, request):

        if request.method == 'POST' and request.FILES.get('video'):
            # read config file
            with open("config.yaml", "r") as stream:
                try:
                    config_file = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    logging.error(exc)

            video_file = request.FILES['video']
            user_name = request.data.get('user_name')

            try:
                if settings.USE_SPACES:

                    upload = UploadedVideos(username=user_name,
                                            video_file=video_file)
                    uploaded_video_url = upload.video_file.url
                    uploaded_video_url = uploaded_video_url.split("?")[0]
                    upload.video_file_url = uploaded_video_url
                    upload.save()
                    return JsonResponse({'message': 'Video uploaded successfully on Digital Ocean Space',
                                         'video_url': uploaded_video_url},
                                        status=200)
                else:
                    fs = FileSystemStorage()
                    filename = fs.save(video_file.name, video_file)
                    video_url = fs.url(filename)

                    return JsonResponse({'message': 'Video uploaded successfully on Django Server',
                                         'video_url': video_url},
                                        status=200)
            except Exception as e:
                return JsonResponse({'message': 'Invalid request {error}'.format(error=e)}, status=400)


class DashboardUsersView(APIView):
    def get(self, request):
        try:
            all_user_details = {}
            all_users = UserProfile.objects.all()
            for user in all_users:
                user_preference = UserPreference.objects.filter(user_id=user.id)

                if user_preference:
                    all_user_details.update({str(user.id): {
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "birth_date": user.birth_date,
                        "categories": user_preference[0].user_categories,
                        "video_history": user_preference[0].user_video_history
                    }})
                else:
                    all_user_details.update({str(user.id): {
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "birth_date": user.birth_date,
                        "categories": {},
                        "video_history": {}
                    }})

            return Response(all_user_details,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error Fetching API Details"},
                            status=status.HTTP_400_BAD_REQUEST)


class DashboardVideosView(APIView):
    def get(self, request):
        all_video_details = {}
        all_videos = VideoMetaData.objects.all()

        for videos in all_videos:
            video_details = VideoDetails.objects.filter(video_id=videos.video_id)

            if video_details:
                all_video_details.update({str(videos.video_id): {
                    "video_url": videos.video_url,
                    "video_title": videos.video_title,
                    "video_duration": videos.video_duration,
                    "likes": videos.video_likes,
                    "dislikes": videos.video_dislikes,
                    "video_transcription": videos.video_transcription,
                    "video_category": videos.video_category,
                    "video_information": videos.video_information,
                    "vpa_pipeline_status": video_details[0].vpa_pipeline_status,
                    "vpa_video_status": video_details[0].vpa_video_status
                }})
            else:
                all_video_details.update({str(videos.video_id): {
                    "video_url": videos.video_url,
                    "video_title": videos.video_title,
                    "video_duration": videos.video_duration,
                    "likes": videos.video_likes,
                    "dislikes": videos.video_dislikes,
                    "video_transcription": videos.video_transcription,
                    "video_category": videos.video_category,
                    "video_information": videos.video_information,
                    "vpa_pipeline_status": {},
                    "vpa_video_status": {}
                }})

        return Response(all_video_details, status=status.HTTP_200_OK)
