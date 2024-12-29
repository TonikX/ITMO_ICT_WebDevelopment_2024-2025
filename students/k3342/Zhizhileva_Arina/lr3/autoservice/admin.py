from django.contrib import admin
from .models import Customer, Car, Employee, Service, Order, OrderDetails, Payment, Qualification

admin.site.register(Customer)
admin.site.register(Car)
admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Payment)
admin.site.register(Qualification)

