from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Commodity, CommodityName
from django.db.models import Max

from .models import Commodity
from .serializers import CommoditySerializer, CommodityCreateSerializer, CommodityDefaultSerializer, CommodityASerializer


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
            commodity_name = commodity.name.name
            if commodity_name not in grouped_commodities:
                grouped_commodities[commodity_name] = []
            grouped_commodities[commodity_name].append(commodity)

        # Serialize each group separately
        serialized_data = {}
        for commodity_name, commodities in grouped_commodities.items():
            serialized_data[commodity_name] = self.serializer_class(commodities, many=True).data

        return Response(serialized_data)
    

class CommodityCreateAPIView(generics.CreateAPIView):
    queryset = Commodity.objects.all()
    serializer_class = CommodityCreateSerializer



class LatestCommodityListAPIView(generics.ListAPIView):
    serializer_class = CommodityDefaultSerializer

    def get_queryset(self):
        # Get the latest commodity entry for each commodity name
        latest_commodities = Commodity.objects.order_by('name', '-time').distinct('name')

        return latest_commodities
    

class CommodityDataAPIView(generics.ListAPIView):
    serializer_class = CommodityASerializer

    def get_queryset(self):
        # Get the commodity name from the request parameters
        commodity_name = self.request.query_params.get('name')

        # Check if the commodity name is provided
        if not commodity_name:
            return Commodity.objects.none()

        try:
            # Query the CommodityName instance by name
            commodity_name_instance = CommodityName.objects.get(name=commodity_name)
            print(commodity_name_instance)
            # Query Commodity instances related to the CommodityName
            commodity_data = Commodity.objects.filter(name=commodity_name_instance)
            return commodity_data
        except CommodityName.DoesNotExist:
            # If the commodity name does not exist, return an empty queryset
            return Commodity.objects.none()

    def list(self, request, *args, **kwargs):
        # Override the list method to return a custom response
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

