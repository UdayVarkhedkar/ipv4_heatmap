import csv
import math
from decimal import *

from django.core.management.base import BaseCommand, CommandError
from api.models import IPLocation


class Command(BaseCommand):
    help = 'Deletes existing ip locations and re-imports all ip locations from the provided CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='?', default='ipv4_locations.csv')
        parser.add_argument('batch_size', nargs='?', default=10000)

    def handle(self, *args, **options):
        # Delete all existing IP Locations
        IPLocation.objects.all().delete()
        
        # List of IPLocation objects to be bulk saved
        ip_locations = []

        # Open CSV File
        with open(options['file_name'], 'r', newline='') as csvfile:
            ip_location_reader = csv.reader(csvfile, delimiter=',')
            
            # Use enumerate for built-in counter
            for counter, ip_location in enumerate(ip_location_reader):

                # Retrieve IP network and location data with checks for data validity
                network = ip_location[0]
                if network == 'network' or not network:
                    print(f"Row { counter } doesn't have an associated network")
                    continue

                if ip_location[7]:
                    ip_latitude = Decimal(ip_location[7])
                else:
                    print(f"{ network } does not have an associated latitude")
                    continue

                if ip_location[8]:
                    ip_longitude = Decimal(ip_location[8])
                else:
                    print(f"{ network } does not have an associated longitude")
                    continue

                if ip_latitude < -90 or ip_latitude > 90 or ip_longitude < -180 or ip_longitude > 180:
                    print(f"{ network } does not have possible latitude/longitude values")

                # Append IPLocation object instance to ip_locations list. 
                # Note: This does not save the IPLocation object
                ip_locations.append(IPLocation(
                    ip_network = network,
                    latitude = ip_latitude,
                    longitude = ip_longitude
                ))

                # Uses counter to calculate current batch size of ip_locations (as opposed to checking length of ip_locations)
                # Bulk saves all IPLocation objects in ip_locations
                # Flushes ip_locations
                if counter % int(options['batch_size']) == 0:
                    IPLocation.objects.bulk_create(ip_locations)
                    ip_locations = []
            
            # Bulk save IPLocation objects remaining if number of rows in CSV isn't evenly divisible by batch_size
            IPLocation.objects.bulk_create(ip_locations)