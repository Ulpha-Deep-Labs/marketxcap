from django.urls import path, include
from .views import CommodityListCreateView, CommodityDetailView

urlpatterns = [
   path("", CommodityListCreateView.as_view(), name="commodity-list-create"),
   path("<int:pk>/", CommodityDetailView.as_view(), name="commodity-detail"),
]       