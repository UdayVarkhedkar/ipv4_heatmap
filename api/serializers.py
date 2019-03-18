from api.models import IPLocation
from rest_framework import serializers

class IPLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPLocation
        fields = ('ip_network', 'latitude', 'longitude')