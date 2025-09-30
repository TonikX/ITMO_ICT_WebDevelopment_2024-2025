from django.contrib import admin
from .models import (
    Client, Employee, CarWorkshop,
    JobPosition, Automobile, Model, Contract,
    Service, Detail, CarDetail, DetailsFromClient,
    DistributionOfWork, DetailInService,
)


admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(CarWorkshop)
admin.site.register(JobPosition)
admin.site.register(Automobile)
admin.site.register(Model)
admin.site.register(Contract)
admin.site.register(Service)
admin.site.register(Detail)
admin.site.register(CarDetail)
admin.site.register(DetailsFromClient)
admin.site.register(DistributionOfWork)
admin.site.register(DetailInService)
