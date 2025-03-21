from django.contrib import admin

from .models import Owner, ExampleModel, Publisher
from .models import Car
from .models import Ownership
from .models import Driver_license

admin.site.register(Owner)
admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(Driver_license)
admin.site.register(ExampleModel)
admin.site.register(Publisher)