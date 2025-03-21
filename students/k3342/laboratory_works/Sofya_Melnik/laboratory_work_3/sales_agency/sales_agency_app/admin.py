from django.contrib import admin
from .models import Client, Service, PriceList, ServiceOrder, PaymentOrder, Employee, Position, PositionEmployee, Order

admin.site.register(Client)
admin.site.register(Service)
admin.site.register(ServiceOrder)
admin.site.register(PriceList)
admin.site.register(Order)
admin.site.register(PaymentOrder)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(PositionEmployee)
