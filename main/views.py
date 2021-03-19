from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from . import serializers


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # import geopy.distance

        # coords_1 = (52.2296756, 21.0122287)
        # coords_2 = (52.406374, 16.9251681)

        # print(vincenty(coords_1, coords_2).km)

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
            "user": serializers.UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

# Create your views here.
# @api_view(['GET'])
# def getUserById(request, id):
#     print('fffffffffffffffffffffffffffff')
#     serializer = serializers.ArticleSerializer(Article.objects.all()[:100], many=True)

#     return Response(serializer.data)