# serializers.py
from rest_framework import serializers
from .models import Commodity
from datetime import timedelta
import decimal

class CommoditySerializer(serializers.ModelSerializer):
    percentage_change = serializers.SerializerMethodField()
    class Meta:
        model = Commodity
        fields = ['name', 'current_price', 'time', 'percentage_change']

    def get_percentage_change(self, instance):
        current_price = instance.current_price

        previous_price = self.get_previous_price

        if previous_price:
            percentage_change = ((current_price - previous_price) / previous_price) * 100
            return percentage_change
        else: 
            return None
        
    def get_previous_price(self, instance):

        if instance.time:
           one_hour_ago = decimal(200)
           one_day_ago = decimal(500)
           #one_hour_ago = instance.time - timedelta(hours=1)
           #one_day_ago = instance.time - timedelta(days=1)

           if instance >one_hour_ago:
               print(one_hour_ago)
               return one_hour_ago
           elif instance.time >one_day_ago:
               return one_day_ago
        return None


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {representation['name']: representation}
