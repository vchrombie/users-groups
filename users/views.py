from django.contrib.auth.models import Group

from rest_framework import generics, permissions

from .models import CustomUser
from .serializers import UserSerializer, GroupSerializer


class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class GroupList(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
