import json

from django.test import TestCase

from .models import IPLocation

durham = (35.994034, -78.898621)
paris = (48.852754, 2.347039)
melbourne = (-37.822527, 144.980063)
buenos_aires = (-34.593175, -58.442160)
atlantic_ocean = (29.956295, -44.907266)

class IPLocationAPITest(TestCase):
    def setUp(self):
        IPLocation.objects.create(ip_network='durham', latitude=36, longitude=-79)
        IPLocation.objects.create(ip_network='paris', latitude=49, longitude=2.5)
        IPLocation.objects.create(ip_network='melbourne', latitude=-38, longitude=145)
        IPLocation.objects.create(ip_network='buenos aires', latitude=-35, longitude=-58)


    def _get_surrounding_latlong_boundaries(self, coordinate):
        latitude, longitude = coordinate
        latitude_min = (latitude - 0.5)
        latitude_max = (latitude + 0.5)
        longitude_min = (longitude - 0.5)
        longitude_max = (longitude + 0.5)
        return {'latitude1': latitude_min,
                'latitude2': latitude_max,
                'longitude1': longitude_min,
                'longitude2': longitude_max}

    def _reverse_latlong_boundaries(self, coordinates):
        latitude_min = coordinates['latitude1']
        latitude_max = coordinates['latitude2']
        coordinates['latitude1'] = latitude_max
        coordinates['latitude2'] = latitude_min
        return coordinates

    def test_durham_ip_locations(self):
        api_parameters = self._get_surrounding_latlong_boundaries(durham)
        response = self.client.get('/api/?', api_parameters)
        self.assertEqual(response.status_code, 200)
        try:
            response_json = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("First argument is not valid JSON: %r" % response.content)
        self.assertEqual(response_json["status"], "Success")
        self.assertEqual(int(response_json["hits"]), 1)

    def test_paris_ip_locations(self):
        api_parameters = self._get_surrounding_latlong_boundaries(paris)
        response = self.client.get('/api/?', api_parameters)
        self.assertEqual(response.status_code, 200)
        try:
            response_json = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("First argument is not valid JSON: %r" % response.content)
        self.assertEqual(response_json["status"], "Success")
        self.assertEqual(int(response_json["hits"]), 1)

    def test_melbourne_ip_locations(self):
        api_parameters = self._get_surrounding_latlong_boundaries(melbourne)
        response = self.client.get('/api/?', api_parameters)
        self.assertEqual(response.status_code, 200)
        try:
            response_json = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("First argument is not valid JSON: %r" % response.content)
        self.assertEqual(response_json["status"], "Success")
        self.assertEqual(int(response_json["hits"]), 1)

    def test_buenos_aires_ip_locations(self):
        api_parameters = self._get_surrounding_latlong_boundaries(buenos_aires)
        response = self.client.get('/api/?', api_parameters)
        self.assertEqual(response.status_code, 200)
        try:
            response_json = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("First argument is not valid JSON: %r" % response.content)
        self.assertEqual(response_json["status"], "Success")
        self.assertEqual(int(response_json["hits"]), 1)

    def test_atlantic_ip_locations(self):
        api_parameters = self._get_surrounding_latlong_boundaries(atlantic_ocean)
        response = self.client.get('/api/?', api_parameters)
        self.assertEqual(response.status_code, 200)
        try:
            response_json = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("First argument is not valid JSON: %r" % response.content)
        self.assertEqual(response_json["status"], "Failure")
        
    def test_reverse_latlong_coordinates(self):
        api_parameters = self._get_surrounding_latlong_boundaries(durham)
        api_parameters = self._reverse_latlong_boundaries(api_parameters)
        response = self.client.get('/api/?', api_parameters)
        self.assertEqual(response.status_code, 200)
        try:
            response_json = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("First argument is not valid JSON: %r" % response.content)
        self.assertEqual(response_json["status"], "Success")
        self.assertEqual(int(response_json["hits"]), 1)