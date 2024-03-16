# serializers.py
from rest_framework import serializers
from .models import Commodity


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity

