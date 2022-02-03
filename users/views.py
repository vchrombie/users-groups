from django.contrib.auth.models import Group

from rest_framework import generics, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserSerializer, GroupSerializer

import requests

TOKEN_OBTAIN_ENDPOINT = 'http://localhost:8080/api/token/'
CART_ENDPOINT = 'http://localhost:8080/cart/'

USERNAME, PASSWORD = '+918186866445', 'root'


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


@api_view()
@authentication_classes([])
@permission_classes([])
def get_cart_items(request):
    response = requests.post(
        TOKEN_OBTAIN_ENDPOINT,
        data={
            'username': USERNAME,
            'password': PASSWORD
        },
        headers={
            "Accept": "application/json",
        },
        cookies={},
        auth=(),
    )

    token = response.json()['access']

    response = requests.get(
        CART_ENDPOINT,
        data={},
        headers={
            'Authorization': f'Bearer {token}'
        },
        cookies={},
        auth=(),
    )

    return Response(response.json())
