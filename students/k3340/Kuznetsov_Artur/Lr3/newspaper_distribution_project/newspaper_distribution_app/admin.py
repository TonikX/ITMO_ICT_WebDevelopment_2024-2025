from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Newspaper)
admin.site.register(PrintingHouse)
admin.site.register(PostOffice)
admin.site.register(Edition)
admin.site.register(Distribution)
