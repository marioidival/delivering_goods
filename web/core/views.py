from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Map
from core.serializers import MapSerializer



def calculate_route_price(autonomy, gas, distance):
    '''Calculates the value of the route, based on the autonomy of the truck

    params: autonomy, Km/l
    params: gas, price/l
    params: distance, value in Km

    returns coast, The price of route.
    '''
    coast = (distance / float(autonomy)) * float(gas)
    return coast


class CreateMapView(CreateAPIView):
    serializer_class = MapSerializer


@api_view()
def mesh_view(request):
    map_name = request.query_params.get('map')
    map = get_object_or_404(Map, name=map_name)

    root = request.query_params.get('root')
    destination = request.query_params.get('destination')
    autonomy = request.query_params.get('autonomy')
    gas = request.query_params.get('gas')

    try:
        distance, route = map.process_mesh(root, destination)
    except:
        return Response({'detail': 'Route Not Found!'}, status=404)

    route = ' '.join(route)
    coast = calculate_route_price(autonomy, gas, distance)

    response = 'Route {route} coast {coast:.2f}'.format(
        route=route, coast=coast
    )
    return Response(response)

