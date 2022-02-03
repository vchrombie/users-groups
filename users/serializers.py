from django.contrib.auth.models import Group

from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'groups',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)
