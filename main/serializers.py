# -*- coding: utf-8 -*-

from rest_framework import serializers

from rest_framework.permissions import IsAuthenticated
from django.db import models
from . import models as main_models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
from dating import settings
User = get_user_model()


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'aituUserId': self.user.aituUserId})
        data.update({'first_name': self.user.first_name})
        data.update({'last_name': self.user.last_name})
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('aituUserId', 'first_name', 'last_name', 'id')


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
        userProfile = main_models.UserProfile.objects.create(
            user = validated_data['user'],
            gender = validated_data['gender'],
            city = validated_data['city'],
            birth_date = validated_data['birth_date'],
            avatar = validated_data['avatar'],
            latitude = validated_data['latitude'],
            longitude = validated_data['longitude'],
            breefly = validated_data['breefly'],
        )

        return userProfile

    def update(self, instance, validated_data):
        instance = main_models.UserProfile.objects.get(validated_data['user'])
        instance.gender = validated_data['gender']
        instance.city = validated_data['city']
        instance.birth_date = validated_data['birth_date']
        # instance.avatar = validated_data['avatar']
        instance.latitude = validated_data['latitude']
        instance.longitude = validated_data['longitude']
        instance.breefly = validated_data['breefly']

        instance.save()

        return instance


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


# User serializer
class UsersListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        print("aaaaaaaaaaa", self.context)
        request = self.context['request']
        return request.build_absolute_uri(obj.avatar.url)

    class Meta:
        model = main_models.UserProfile
        fields = '__all__'


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(aituUserId=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.aituUserId = validated_data['aituUserId']

        instance.save()

        return instance


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.City
        fields = '__all__'
