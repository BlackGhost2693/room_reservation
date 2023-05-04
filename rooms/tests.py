import json
from datetime import date
from pathlib import Path
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from .views import AvailableReservationViewSet


FIXTURE_DIR = str(Path(__file__).resolve().parent.parent) + "/sample_data.json"


class Test(TestCase):

    fixtures = [FIXTURE_DIR,]

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_available_reservation_all(self):
        request = self.factory.get("/room/available/")
        response = AvailableReservationViewSet.as_view(
            {'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_available_reservation_single(self):
        request = self.factory.get("/room/available/1/")
        response = AvailableReservationViewSet.as_view(
            {'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_reserve_single(self):
        data = {
            "date": date.today().strftime('%Y-%m-%d'),
            "room": 1,
            "reservationist": "Dani",
            "phone": "09123456789"
        }
        client = APIClient()
        request = client.post(
            '/room/reserve/', json.dumps(data), content_type='application/json')
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.data, {"status": "Done."})

    def test_reserve_bulk(self):
        data = [{
            "date": date.today().strftime('%Y-%m-%d'),
            "room": room,
            "reservationist": "Dani",
            "phone": "09123456789"
        } for room in [1,2,3]]
        client = APIClient()
        request = client.post(
            '/room/reserve/', json.dumps(data), content_type='application/json')
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.data, {"status": "Done."})
