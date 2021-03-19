# -*- coding: utf-8 -*-

from rest_framework import serializers

# from .models_moodle import MdlGradeItems
from .models import Article, Image, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = (
        #     'class_id',
        #     'date_from',
        #     'date_to'
        # )
        # read_only_fields = (
        #     'class_id',
        #     'date_from',
        #     'date_to'
        # )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
