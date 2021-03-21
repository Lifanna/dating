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
from django.db.models import Count



class UsersListApi(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UsersListSerializer

    def get_object(self, userId):
        return get_object_or_404(models.User.objects.filter(user_id=userId))

    def get(self, request, *args,  **kwargs):
        offset = kwargs["offset"]
        limit = 5
        user_profile = models.UserProfile.objects.exclude(id=request.user.id)[offset:offset + limit]

        serializer = self.serializer_class(user_profile, many=True, context={'request': request})

        return Response(serializer.data)


class UsersNearestApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_profile = models.UserProfile.objects.get(id=request.user.id)
        
        friends = models.UserProfile.objects.filter(
            latitude__lte=user_profile.latitude, 
            latitude__gte=user_profile.latitude,
            longitude__lte=user_profile.longitude, 
            longitude__gte=user_profile.longitude
        )
        friend_profile = models.UserProfile.objects.exclude(id=request.user.id)
        user_coords = tuple(user_profile.latitude, user_profile.longitude) # (lat, lon)
        friend_coords = tuple(user_profile.latitude, user_profile.longitude)

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

    def get_queryset(self):
        return models.User.objects.all()

    def get(self, request, *args,  **kwargs):
        user_profile = self.get_object(request.user.id)
        serializer = self.serializer_class(user_profile)
        user_serializer = serializers.UserSerializer(request.user)

        return Response({"userInfo": user_serializer.data, "userProfile": serializer.data})

    def post(self, request, *args,  **kwargs):
        # models.City.objects.get_or_create(name="Karaganda")
        # request.FILES
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save()

        return Response({
            "user": serializers.RegisterProfileSerializer(user_profile, context=self.get_serializer_context()).data,
        })
    
    def put(self, request, *args, **kwargs):
        user_to_update = self.get_object(request.user.id)
        user_to_update.gender = request.data.get("gender")
        user_to_update.city = models.City.objects.get(id=request.data.get("city"))
        user_to_update.birth_date = request.data.get("birth_date")
        user_to_update.avatar = request.data.get("avatar")
        user_to_update.latitude = request.data.get("latitude")
        user_to_update.longitude = request.data.get("longitude")
        user_to_update.breefly = request.data.get("breefly")
        user_to_update.save()

        return Response({
            "user": serializers.RegisterProfileSerializer(user_to_update, context=self.get_serializer_context()).data,
        })


class UserAvatarApi(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RegisterProfileSerializer

    def get_object(self, userId):
        return get_object_or_404(models.UserProfile.objects.filter(user_id=userId))

    def get_queryset(self):
        return models.User.objects.all()

    def get(self, request, *args,  **kwargs):
        pass
        # user_profile = self.get_object(request.user.id)
        # serializer = self.serializer_class(user_profile)
        # user_serializer = serializers.UserSerializer(request.user)

        # return Response({"userProfile": serializer.data})

    def post(self, request, *args,  **kwargs):
        user_to_update = models.User.objects.get(request.user.id)
        user_to_update.avatar = request.data.get("avatar")
        user_to_update.save()
        
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user_profile = serializer.save()

        return Response({
            "user": serializers.UserProfileSerializer(user_to_update, context=self.get_serializer_context()).data,
        })


class CommentsApi(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_object(self, userId):
        return get_object_or_404(models.Comment.objects.filter(user_id=userId))

    def get(self, request, *args,  **kwargs):
        userComments = models.Comment.objects.values('user_id').annotate(total=Count('author_id'))

        # comments = models.Comment.objects.filter(user_id=kwargs['userId'])
        # serializer = serializers.CommentSerializer(userComments, many=True)
        return Response({"userComments": userComments})

    def post(self, request, *args,  **kwargs):
        comment_serializer = self.serializer_class(data=request.data)

        comment_serializer.is_valid(raise_exception=True)
        comment_serializer.save()

        return Response(data=comment_serializer.data)


class LikeApi(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LikeSerializer
    
    def get(self, request, *args,  **kwargs):
        # likes = models.Like.objects.filter(user_id=kwargs['userId'])
        # count = likes.count()
        userLikes = models.Like.objects.values('user_id').annotate(total=Count('author_id'))

        return Response({"userLikes": userLikes})
    
    def post(self, request, *args,  **kwargs):
        like_serializer = self.serializer_class(data=request.data)

        like_serializer.is_valid(raise_exception=True)
        like_serializer.save()

        return Response(data=like_serializer.data)


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


class CityApi(APIView):
    serializer_class = serializers.CitySerializer

    def get(self, request, *args,  **kwargs):
        user_profile = models.City.objects.all()

        serializer = self.serializer_class(user_profile, many=True)

        return Response(serializer.data)
