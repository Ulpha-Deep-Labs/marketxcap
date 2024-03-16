from django.db import models

# Create your models here.
class Commodity(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    highest_price = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_price = models.DecimalField(max_digits=10, decimal_places=2)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.commodity_name} - ₦{self.current_price} (Last updated: {self.last_updated})"