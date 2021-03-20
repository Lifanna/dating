from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from . import serializers
from haversine import haversine, Unit
from django.shortcuts import get_object_or_404
from . import models


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        lyon = (45.7597, 4.8422) # (lat, lon)
        paris = (48.8567, 2.3508)

        distance = haversine(lyon, paris)

        print("DISTANCE:       ", distance)

        content = {'message': 'Hello, World!'}
        return Response(content)


class RegisterApi(GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def get(self, request):
        return Response({"success": True})

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": serializers.UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class RegisterProfileApi(GenericAPIView):
    serializer_class = serializers.RegisterProfileSerializer

    def get(self, request):
        return Response({"success": True})

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save()

        return Response({
            "user": serializers.UserSerializer(user_profile, context=self.get_serializer_context()).data,
        })


class CommentsApi(APIView):
    serializer_class = serializers.CommentSerializer

    def get_object(self, userId):
        obje = models.Comment.objects.all()
        print(obje)
        return get_object_or_404(models.Comment.objects.filter(user_id=userId))

    def get(self, request, *args,  **kwargs):
        comment = self.get_object(kwargs['userId'])
        serializer = comment

        return Response(serializer.data)

    def post(self, request, *args,  **kwargs):
        comment_serializer = self.serializer_class(data=request.data)

        comment_serializer.save()

        return Response(data=comment_serializer.data, status=status.HTTP_201_CREATED)
