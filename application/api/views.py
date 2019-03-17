from decimal import Decimal

from django.http import JsonResponse, HttpResponseNotAllowed
from django.core import serializers

from .models import IPLocation


def index(request):
    if request.method == "GET":
        # Get querystring parameter values
        latitude1 = Decimal(request.GET.get("latitude1", 35.5))
        longitude1 = Decimal(request.GET.get("longitude1", -78.5))
        latitude2 = Decimal(request.GET.get("latitude2", 35.75))
        longitude2 = Decimal(request.GET.get("longitude2", -78.75))

        # Establish min/max latitude/longitude values for Postgresql Between
        min_latitude = min(latitude1, latitude2)
        max_latitude = max(latitude1, latitude2)
        min_longitude = min(longitude1, longitude2)
        max_longitude = max(longitude1, longitude2)

        # Ensure provided longitude/latitude values are within possible bounds
        if min_latitude < -90 or max_latitude > 90 or min_longitude < -180 or max_longitude > 180:
            return JsonResponse({"status": "Failure", "message": "Latitude of longitude values exceeded possible bounds."})


        # Retrieve ip locations within geographic boundary and count
        ip_locations = IPLocation.objects.filter(latitude__range=(min_latitude, max_latitude), longitude__range=(min_longitude, max_longitude))
        ip_locations_count = ip_locations.count()

        if ip_locations_count == 0:
            return JsonResponse({"status": "Failure", "message": "No ip networks were found within the given area."})

        # Serialize ip locations queryset for JsonResponse
        serialized_ip_locations = serializers.serialize("json", ip_locations, fields=("ip_network", "latitude", "longitude"))

        return JsonResponse({"status": "Success","hits": ip_locations_count, "ip_locations": serialized_ip_locations})
    else:
        return HttpResponseNotAllowed