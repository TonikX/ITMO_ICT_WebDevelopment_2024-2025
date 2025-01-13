from django.contrib import admin
from .models import User
from .models import Truck
from .models import Comments
from .models import Race
from .models import Driver
from .models import Car
# Register your models here.


admin.site.register(User)
admin.site.register(Truck)
admin.site.register(Driver)
admin.site.register(Race)
admin.site.register(Comments)
admin.site.register(Car)

