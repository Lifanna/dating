from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from . import serializers


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from haversine import haversine, Unit

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
            "user": serializers.UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

# Create your views here.
# @api_view(['GET'])
# def getUserById(request, id):
#     print('fffffffffffffffffffffffffffff')
#     serializer = serializers.ArticleSerializer(Article.objects.all()[:100], many=True)

#     return Response(serializer.data)