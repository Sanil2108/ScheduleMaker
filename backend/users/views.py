from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer

from users.models import User

class CreateUser(APIView):
  def post(self, request):
    user_serializer = UserSerializer(data = request.data)
    user_serializer.is_valid(raise_exception = True)

    user = user_serializer.create()
    try:
      user.full_clean()
    except ValidationError as e:
      return Response('User with this email already exists', status = status.HTTP_400_BAD_REQUEST)

    user.save()

    return Response(status = status.HTTP_201_CREATED)

class LoginUser(APIView):
  def post(self, request):
    user = User.objects.get_auth_user_with_password(request.META.get('HTTP_AUTHORIZATION'))
    if user is None:
      user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
      
    if user is None:
      return Response('No such user', status = status.HTTP_401_UNAUTHORIZED)

    user.update_and_get_token()

    return Response(UserSerializer(user).data)