from django.contrib import admin
from .models import Client, Car, Worker, Service, Order, OrderInfo, PayProcess, Qualification

admin.site.register(Client)
admin.site.register(Car)
admin.site.register(Worker)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderInfo)
admin.site.register(PayProcess)
admin.site.register(Qualification)

