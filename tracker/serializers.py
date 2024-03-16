# serializers.py
from rest_framework import serializers
from .models import Commodity, CommodityName
from datetime import timedelta
import decimal

class CommodityNameSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CommodityName
        fields = ['name', 'symbol']


class CommoditySerializer(serializers.ModelSerializer):
    name = CommodityNameSerialzer()
    one_hour_percentage_change = serializers.SerializerMethodField()
    one_day_percentage_change = serializers.SerializerMethodField()
    one_week_percentage_change = serializers.SerializerMethodField()
    

    class Meta:
        model = Commodity
        fields = ['id', 'name', 'current_price',  'time', 'one_hour_percentage_change', 'one_week_percentage_change', 'one_day_percentage_change']

    def get_one_hour_percentage_change(self, instance):
        current_price = instance.current_price
        previous_price = instance.price_1_hour_ago  # Get the previous price
        if previous_price is not None and current_price is not None and previous_price != 0:
            percentage_change = ((current_price - previous_price) / previous_price) * 100
            return percentage_change
        else:
            return None  # If any price is None or previous price is zero, return None

    def get_one_day_percentage_change(self, instance):
        current_price = instance.current_price
        previous_price = instance.price_1_day_ago  # Get the previous price
        if previous_price is not None and current_price is not None and previous_price != 0:
            percentage_change = ((current_price - previous_price) / previous_price) * 100
            return percentage_change
        else:
            return None  # If any price is None or previous price is zero, return None
        
    def get_one_week_percentage_change(self, instance):
        current_price = instance.current_price
        previous_price = instance.price_7_days_ago  # Get the previous price
        if previous_price is not None and current_price is not None and previous_price != 0:
            percentage_change = ((current_price - previous_price) / previous_price) * 100
            return percentage_change
        else:
            return None  # If any price is None or previous price is zero, return None





class CommodityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ['name', 'current_price', 'time']
        read_only_fields = ['price_1_hour_ago', 'price_1_day_ago', 'price_7_days_ago']

    def create(self, validated_data):
        # Extract the commodity_name instance from the validated data
        commodity_name_instance = validated_data.pop('name')
        # Create the commodity using the remaining validated data
        commodity = Commodity.objects.create(name=commodity_name_instance, **validated_data)
        return commodity