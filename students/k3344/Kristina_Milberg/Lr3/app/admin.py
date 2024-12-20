from django.contrib import admin

from .models import (Agency, BrokerCompany, Broker,
                     BrokerInfo, ProductGroup, Manufacturer,
                     Product, Order, Transaction, BatchProduct)

# Register your models here.
admin.site.register(Agency)
admin.site.register(BrokerCompany)
admin.site.register(Broker)
admin.site.register(BrokerInfo)
admin.site.register(ProductGroup)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(BatchProduct)
