from django.urls import path, include
from .views import CommodityListCreateView, CommodityPriceListCreateView

urlpatterns = [
   path("", CommodityListCreateView.as_view(), name="commodity-list-create"),
   path("<int:pk>/", CommodityPriceListCreateView.as_view(), name='commodity-details'),
]       



