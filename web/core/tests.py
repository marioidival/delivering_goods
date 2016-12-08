from django.test import TestCase
from rest_framework.test import APIClient
from core.models import Map


class TestAPIMap(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_map(self):
        'Create correctly a map with mash'
        data = {'name': 'test map', 'mesh': 'A B 10 C D 11 E D 15'}

        response = self.client.post('/api/map', data)
        self.assertEqual(201, response.status_code)

    def test_create_map_without_name_raises_400(self):
        'Raises 400 STATUS Code without map name'
        data = {'mesh': 'A B 10 C D 11 E D 15'}

        response = self.client.post('/api/map', data)
        self.assertEqual(400, response.status_code)

    def test_create_map_without_mesh_raises_400(self):
        'Raises 400 STATUS Code without mesh'
        data = {'name': 'test map'}

        response = self.client.post('/api/map', data)
        self.assertEqual(400, response.status_code)

    def test_create_map_with_duplicate_map_name(self):
        'Its not possible create map with name duplicated'
        data = {'name': 'test map', 'mesh': 'A B 10 C D 11 E D 15'}

        # Simulate Twice requests
        response = self.client.post('/api/map', data)
        response = self.client.post('/api/map', data)

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.content,
            b'{"name":["map with this name already exists."]}'
        )
