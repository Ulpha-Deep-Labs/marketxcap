from rest_framework import generics
from rest_framework.response import Response

from .models import Commodity, Price
from .serializers import CommoditySerializer, PriceSerializer


# Create your views here.
class CommodityListCreateView(generics.ListCreateAPIView):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer


class CommodityPriceListCreateView(generics.ListCreateAPIView):
    serializer_class = PriceSerializer

    def get_queryset(self):
        return Price.objects.filter(commodity=self.kwargs["pk"])
