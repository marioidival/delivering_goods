from django.conf.urls import url
from core.views import CreateMapView, mesh_view


urlpatterns = [
    url(r'^api/map', CreateMapView.as_view(), name='create_map'),
    url(r'^api/mesh', mesh_view, name='get_mesh'),
]
