import decimal

from rest_framework import generics, status
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

    def post(self, request, *args, **kwargs):
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            commodity = Commodity.objects.filter(id=self.kwargs["pk"]).first()
            commodity.update_prices(decimal.Decimal(serializer.data["amount"]))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
