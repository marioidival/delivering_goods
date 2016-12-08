from django.db import models
from core.find_route import FindRoute
from core.process_text import TextRouteProcess


class Map(models.Model):
    name = models.CharField(max_length=100)
    mesh = models.TextField()

    def save(self, *args, **kwargs):
        # Remove all \r\n from mesh text
        self.mesh = self.mesh.replace('\r\n', ' ')
        return super(Map, self).save(*args, **kwargs)

    def process_mesh(self, root, destination):
        '''Process `mesh` of `map` and return shortest route with distance'''
        text_processor = TextRouteProcess(self.mesh)
        find_route = FindRoute(text_processor.routes())
        return find_route.shortest_route(root, destination)
