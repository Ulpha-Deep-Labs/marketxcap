from rest_framework import generics

from .models import Commodity
from .serializers import CommoditySerializer


# Create your views here.
class CommodityListCreateView(generics.ListCreateAPIView):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer


class CommodityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
