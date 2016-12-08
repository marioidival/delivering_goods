from rest_framework.serializers import ModelSerializer
from core.models import Map


class MapSerializer(ModelSerializer):

    class Meta:
        model = Map
        fields = '__all__'
