from django.contrib import admin
from .models import PrintShop, Newspaper, PrintRun, PostOffice, Delivery

admin.site.register(PrintShop)
admin.site.register(Newspaper)
admin.site.register(PrintRun)
admin.site.register(PostOffice)
admin.site.register(Delivery)
