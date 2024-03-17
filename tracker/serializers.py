from rest_framework import serializers

from .models import Commodity, Price


class CommoditySerializer(serializers.ModelSerializer):

    class Meta:
        model = Commodity
        fields = "__all__"


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = "__all__"
