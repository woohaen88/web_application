from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import AuthTokenSerializer, UserInSerializer


class UserCreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserInSerializer
