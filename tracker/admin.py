from django.contrib import admin
from .models import Commodity, CommodityName

# Register your models here.
admin.site.register(CommodityName)
admin.site.register(Commodity)