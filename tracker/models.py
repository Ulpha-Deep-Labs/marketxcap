from django.db import models


# Create your models here.
class Commodity(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_change = models.DecimalField(max_digits=10, decimal_places=2)

    def update_prices(self, new_price):
        perc_change = self.calc_perc_change(new_price, self.current_price)
        self.percentage_change = perc_change
        self.current_price = new_price
        self.save()

    def __str__(self):
        return f"{self.name} - ₦{self.symbol}"
    
    @classmethod
    def calc_perc_change(cls, new_price, old_price):
        return ((new_price - old_price) / old_price) * 100
    


class Price(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commodity = models.ForeignKey("Commodity", on_delete=models.CASCADE)
    _at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commodity.name} @ ₦{self.amount} at {self._at}"

