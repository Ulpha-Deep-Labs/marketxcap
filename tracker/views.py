from rest_framework import generics
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Commodity

from .models import Commodity
from .serializers import CommoditySerializer



# Create your views here.
class CommodityListCreateView(generics.ListCreateAPIView):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer


# In your Django app's views.py file


class CommodityDetailsAPIView(generics.ListAPIView):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Group commodities by commodity_name
        grouped_commodities = {}
        for commodity in queryset:
            commodity_name = commodity.name
            if commodity_name not in grouped_commodities:
                grouped_commodities[commodity_name] = []
            grouped_commodities[commodity_name].append(commodity)

        # Serialize each group separately
        serialized_data = {}
        for commodity_name, commodities in grouped_commodities.items():
            serialized_data[commodity_name] = self.serializer_class(commodities, many=True).data

        return Response(serialized_data)

