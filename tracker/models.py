from django.db import models


# Create your models here.
class Commodity(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_change = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ₦{self.symbol}"


class Price(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commodity = models.ForeignKey("Commodity", on_delete=models.CASCADE)
    _at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commodity.name} @ ₦{self.amount} at {self._at}"

