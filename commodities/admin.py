from django.contrib import admin
from .models import Commodity, Price

# Register your models here.
admin.site.register(Commodity)
admin.site.register(Price)