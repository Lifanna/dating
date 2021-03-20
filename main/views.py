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
    # permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UsersListSerializer

    def get_object(self, userId):
        return get_object_or_404(models.User.objects.filter(user_id=userId))

    def get(self, request, *args,  **kwargs):
        user_profile = models.UserProfile.objects.exclude(id=1)
        userLikes = models.Like.objects.values('user_id').annotate(total=Count('author_id'))

        likes = models.Like.objects.raw('''
            select 1 as id, user_id as user, COUNT(author_id) as likes from main_like
            join auth_user on
            auth_user.id = main_like.author_id
            GROUP BY user_id
        ''')

        serializer = self.serializer_class(user_profile, many=True)

        return Response({"user": userLikes, "userProfile": serializer.data})


# class UsersNearestApi(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         user_profile = models.UserProfile.objects.get(id=request.user.id)
        
#         friends = models.UserProfile.objects.filter(
#             latitude__lte=user_profile.latitude, 
#             latitude__gte=user_profile.latitude,
#             longitude__lte=user_profile.longitude, 
#             longitude__gte=user_profile.longitude
#         )
#         friend_profile = models.UserProfile.objects.exclude(id=request.user.id)
#         user_coords = tuple(user_profile.latitude, user_profile.longitude) # (lat, lon)
#         friend_coords = tuple(user_profile.latitude, user_profile.longitude)

#         distance = haversine(lyon, paris)

#         print("DISTANCE:       ", distance)

#         content = {'message': 'Hello, World!'}
#         return Response(content)


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
        user_serializer = serializers.UserSerializer(request.user)

        return Response({"userInfo": user_serializer.data, "userProfile": serializer.data})

    def post(self, request, *args,  **kwargs):
        models.City.objects.get_or_create(name="Karaganda")
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
        userComments = models.Comment.objects.values('user_id').annotate(total=Count('author_id'))

        comments = models.Comment.objects.filter(user_id=kwargs['userId'])
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args,  **kwargs):
        comment_serializer = self.serializer_class(data=request.data)

        comment_serializer.is_valid(raise_exception=True)
        comment_serializer.save()

        return Response(data=comment_serializer.data)


class LikeApi(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LikeSerializer
    
    def get(self, request, *args,  **kwargs):
        likes = models.Like.objects.filter(user_id=kwargs['userId'])
        count = likes.count()
        serializer = serializers.LikeSerializer(likes, many=True)
        return Response({"count": count, "data": serializer.data})
    
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