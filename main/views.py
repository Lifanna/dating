from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from geopy.distance import vincenty

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # import geopy.distance

        # coords_1 = (52.2296756, 21.0122287)
        # coords_2 = (52.406374, 16.9251681)

        # print(vincenty(coords_1, coords_2).km)

        content = {'message': 'Hello, World!'}
        return Response(content)


# Create your views here.
# @api_view(['GET'])
# def getUserById(request, id):
#     print('fffffffffffffffffffffffffffff')
#     serializer = serializers.ArticleSerializer(Article.objects.all()[:100], many=True)

#     return Response(serializer.data)