from decimal import Decimal

from django.http import JsonResponse, HttpResponseNotAllowed
from django.core import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import IPLocation
from api.serializers import IPLocationSerializer

@api_view()
def index(request):
    # Get querystring parameter values
    latitude1 = Decimal(request.GET.get("latitude1", 35.75))
    longitude1 = Decimal(request.GET.get("longitude1", -78.75))
    latitude2 = Decimal(request.GET.get("latitude2", 36.25))
    longitude2 = Decimal(request.GET.get("longitude2", -79.25))

    # Establish min/max latitude/longitude values for Postgresql Between
    min_latitude = min(latitude1, latitude2)
    max_latitude = max(latitude1, latitude2)
    min_longitude = min(longitude1, longitude2)
    max_longitude = max(longitude1, longitude2)

    # Ensure provided longitude/latitude values are within possible bounds
    if min_latitude < -90 or max_latitude > 90 or min_longitude < -180 or max_longitude > 180:
        return Response({"message": "Latitude or longitude values exceeded possible bounds."}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve ip locations within geographic boundary and count
    ip_locations = IPLocation.objects.filter(latitude__range=(min_latitude, max_latitude), longitude__range=(min_longitude, max_longitude))
    ip_locations_count = ip_locations.count()

    if ip_locations_count == 0:
        return Response({"hits": 0})

    # Serialize ip locations queryset for JsonResponse
    serialized_ip_locations = IPLocationSerializer(ip_locations, many=True)

    return Response({"hits": ip_locations_count, "ip_locations": serialized_ip_locations.data})