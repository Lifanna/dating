# -*- coding: utf-8 -*-

from rest_framework import serializers

from rest_framework.permissions import IsAuthenticated
from django.db import models
from . import models as main_models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','aituUserId','password','first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(
            aituUserId=validated_data['aituUserId'], 
            password = validated_data['password'], 
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name']
            
        )
        return user


class RegisterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.UserProfile
        fields = '__all__'

    def create(self, validated_data):
        userProfile = UserProfile.objects.create_user(
            user = validated_data['userId'],
            external_id = validated_data['external_id'],
            gender = validated_data['gender'],
            city = validated_data['city'],
            birth_date = validated_data['birth_date'],
            avatar = validated_data['avatar'],
            latitude = validated_data['latitude'],
            longitude = validated_data['longitude'],
            breefly = validated_data['breefly'],
        )

        return userProfile


# User serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Comment
        fields = '__all__'


# User serializer
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Like
        fields = '__all__'
