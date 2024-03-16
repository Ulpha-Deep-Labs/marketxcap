from django.urls import path, include
from .views import CommodityListCreateView, CommodityDetailsAPIView, CommodityCreateAPIView, LatestCommodityListAPIView

urlpatterns = [
   #path("", CommodityListCreateView.as_view(), name="commodity-list-create"),
   path('', CommodityDetailsAPIView.as_view(), name='commodity-details'),
   path('create/', CommodityCreateAPIView.as_view(), name='create-commodity'),
   path('default/', LatestCommodityListAPIView.as_view(), name='view-commodity'),
]       



