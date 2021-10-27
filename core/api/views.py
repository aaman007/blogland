from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.clients.hatchway import HatchwayClient


class PingAPI(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'status': 'success'})


class BlogListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        tags = request.query_params.get('tags')
        sort_by = request.query_params.get('sortBy', 'id')
        direction = request.query_params.get('direction', 'asc')

        if not tags:
            return Response({
                'error': 'Tags parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        elif sort_by not in ['id', 'reads', 'likes', 'popularity']:
            return Response({
                'error': 'sortBy parameter is invalid'
            }, status=status.HTTP_400_BAD_REQUEST)
        elif direction not in ['asc', 'desc']:
            return Response({
                'error': 'direction parameter is invalid'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'posts': HatchwayClient().fetch_blogs(tags, sort_by, direction)
        })


class TestAPI(APIView):
    def get(self):
        return Response({'status': 'tested'})
