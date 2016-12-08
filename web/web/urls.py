from django.conf.urls import url
from django.views.decorators.cache import cache_page
from core.views import CreateMapView, mesh_view


urlpatterns = [
    url(r'^api/map', CreateMapView.as_view(), name='create_map'),
    url(r'^api/mesh', cache_page(60 * 15)(mesh_view), name='get_mesh'),
]
