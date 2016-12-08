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


class TestGetMesh(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Setup map-mesh from email
        Map.objects.create(
            name='map sp', mesh='A B 10 B D 15 A C 20 C D 30 B E 50 D E 30'
        )
        self.params = {'map': 'map sp', 'root': 'A', 'destination': 'D',
                       'autonomy': '10', 'gas': '2.50'}

    def test_get_shortest_route(self):
        'Returns a object with more shortest route'
        response = self.client.get('/api/mesh', self.params)

        self.assertEqual(200, response.status_code)
        self.assertEqual({'mesh': 'Route A B D coast 6.25'}, response.data)

    def test_get_shortest_route_without_any_params_raise_error(self):
        'Try get a shortest route with missing params raise 404'
        del self.params['gas']
        response = self.client.get('/api/mesh', self.params)

        self.assertEqual(404, response.status_code)
        self.assertIn(b'error', response.content)
