"""
Areas application views for handling area-related API requests.
This module defines API views for listing and retrieving area information.
It includes views for both listing all areas and retrieving details of a specific area.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Area
from .serializers import AreaSerializer


class AreaListView(APIView):
    """
    API view for handling area-related requests.
    This view can be extended to implement specific area functionalities.
    """
    authentication_classes = []  # No authentication required for this view
    permission_classes = []  # No permissions required for this view

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve area information.
        """
        data = Area.active_objects.all()
        serializer = AreaSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AreaDetailView(APIView):
    """
    API view for handling individual area details.
    This view can be extended to implement specific area functionalities.
    """
    authentication_classes = []  # No authentication required for this view
    permission_classes = []  # No permissions required for this view

    
    def get_object(self, slug):
        """
        Retrieve an area object by its primary key.
        """
        try:
            return Area.active_objects.get(slug=slug)
        except Area.DoesNotExist:
            return Http404("Area not found.")

    def get(self, request, slug, *args, **kwargs):
        """
        Handle GET requests to retrieve a specific area by its ID.
        """
        area = self.get_object(slug)
        serializer = AreaSerializer(area)
        return Response(serializer.data, status=status.HTTP_200_OK)
