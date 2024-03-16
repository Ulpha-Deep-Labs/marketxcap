from django.urls import path, include
from .views import CommodityListCreateView, CommodityDetailsAPIView

urlpatterns = [
   #path("", CommodityListCreateView.as_view(), name="commodity-list-create"),
   path('', CommodityDetailsAPIView.as_view(), name='commodity-details'),
]       



