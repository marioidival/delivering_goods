from core.dijkstra import Graph, shortest_path


class FindRoute:

    _graph = Graph()

    def __init__(self, routes):
        self._routes = list(routes)
        self.route_to_graph()

    def route_to_graph(self):
        '''Transform the routes list to graph'''
        routes = iter(self._routes)

        for route in routes:
            self._graph.add_node(route.root)
            self._graph.add_node(route.destination)
            self._graph.add_edge(*route)

    def shortest_route(self, start, end):
        return shortest_path(self._graph, start, end)
