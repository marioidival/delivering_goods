from collections import namedtuple


Route = namedtuple('Route', 'root destination distance')


class TextRouteProcess:
    ''' Class to process mesh raw '''
    _routes = []

    def __init__(self, raw=None):
        if raw:
            self.load_mesh(raw)

    def mesh_raw_to_iterator(self, mesh_raw):
        '''Transform Mesh Raw to iterator'''
        mesh_list = mesh_raw.split()

        for ind in range(0, len(mesh_list) + 1, 3):
            st = ind - 3 if ind > 0 else ind
            mesh_sliced = mesh_list[st:ind]

            if mesh_sliced:
                yield mesh_sliced

    def load_mesh(self, mesh_raw):
        '''Load all mesh to `Route` object'''
        for mesh in self.mesh_raw_to_iterator(mesh_raw):
            *points, distance = mesh
            self._routes.append(Route(*points, int(distance)))

    def routes(self):
        return self._routes


