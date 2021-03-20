from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers
from haversine import haversine, Unit
from django.shortcuts import get_object_or_404
from . import models


class UsersListApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, userId):
        return get_object_or_404(models.User.objects.filter(user_id=userId))

    def get(self, request, *args,  **kwargs):
        print("AD:             ", request.user.aituUserId)
        user = self.get_object(kwargs['userId'])

        user_profile = models.UserProfile.objects.get()

        serializer = self.serializer_class(user_profile)

        return Response(serializer.data)


class UsersNearestApi(APIView):
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


class UserProfileApi(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RegisterProfileSerializer

    def get_object(self, userId):
        return get_object_or_404(models.UserProfile.objects.filter(user_id=userId))

    def get(self, request, *args,  **kwargs):
        user_profile = self.get_object(request.user.id)
        serializer = self.serializer_class(user_profile)

        return Response({"user": request.user.aituUserId, "asd": serializer.data})

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save()

        return Response({
            "user": serializers.RegisterProfileSerializer(user_profile, context=self.get_serializer_context()).data,
        })
    

class CommentsApi(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_object(self, userId):
        return get_object_or_404(models.Comment.objects.filter(user_id=userId))

    def get(self, request, *args,  **kwargs):
        comments = models.Comment.objects.filter(user_id=kwargs['userId'])
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args,  **kwargs):
        comment_serializer = self.serializer_class(data=request.data)

        comment_serializer.is_valid(raise_exception=True)
        comment_serializer.save()

        return Response(data=comment_serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"STATUS": "OK"})
        except Exception as e:
            return Response({"STATUS": "BAD"})


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = serializers.CustomTokenObtainPairSerializer
