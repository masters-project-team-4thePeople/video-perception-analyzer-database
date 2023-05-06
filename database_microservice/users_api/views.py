from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import UserProfile


# Create your views here.
class UserView(APIView):

    def get_user_object(self, username):
        try:
            return UserProfile.objects.get(username=username)
        except Exception as e:
            return None

    def get(self, request):
        # get username
        username_id = request.data.get('username')
        username_instance = self.get_user_object(username_id)

        if not username_instance:
            return Response(
                {
                    "message": "Username Doesn't Exist"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        user_serializer = UserSerializer(username_instance)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        "first_name": "test",
        "last_name": "user",
        "email": "testuser@gmail.com",
        "password": "changeme",
        "birth_date": "2019-09-25",
        "notification_id": ""
        """

        username_id = request.data.get('username')
        username_instance = self.get_user_object(username_id)

        if not username_instance:
            return Response(
                {
                    "message": "Username Doesn't Exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data = {}

        if request.data.get('first_name'):
            user_data.update(
                {'first_name': request.data.get('first_name')}
            )

        if request.data.get('last_name'):
            user_data.update(
                {'last_name': request.data.get('last_name')}
            )

        if request.data.get('email'):
            user_data.update(
                {'email': request.data.get('email')}
            )

        if request.data.get('password'):
            user_data.update(
                {'password': request.data.get('password')}
            )

        if request.data.get('birth_date'):
            user_data.update(
                {'birth_date': request.data.get('birth_date')}
            )

        if request.data.get('notification_id'):
            user_data.update(
                {'notification_id': request.data.get('notification_id')}
            )

        user_serializer = UserSerializer(instance=username_instance,
                                         data=user_data,
                                         partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

