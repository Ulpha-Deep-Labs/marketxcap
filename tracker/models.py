from django.db import models
from django.utils import timezone

# Create your models here.
class Commodity(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now=True)
    price_1_hour_ago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_1_day_ago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_7_days_ago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - ₦{self.current_price} (Last updated: {self.time})"
    
    def save(self, *args, **kwargs):
        one_hour_ago = timezone.now() -timezone.timedelta(hours=1)
        one_day_ago = timezone.now() -timezone.timedelta(days=1)
        seven_days_ago = timezone.now() -timezone.timedelta(days=7)


        one_hour_previous_commodity_price = Commodity.objects.filter(name=self.name, time__lte=one_hour_ago).order_by('-time').first()

        if one_hour_previous_commodity_price:
            self.price_1_hour_ago =one_hour_previous_commodity_price.current_price

        one_day_previous_commodity_price = Commodity.objects.filter(name=self.name, time__lte=one_day_ago).order_by('-time').first()

        if one_day_previous_commodity_price:
            self.price_1_day_ago =one_day_previous_commodity_price.current_price

        
        
        super().save(*args, **kwargs)