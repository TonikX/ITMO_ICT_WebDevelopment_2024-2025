from django.contrib import admin

from alpinist_club_app.models import Mountain, Club, Alpinist, Ascending, AscendingGroup, AlpinistInGroup

admin.site.register(Mountain)
admin.site.register(Club)
admin.site.register(Alpinist)
admin.site.register(Ascending)
admin.site.register(AscendingGroup)
admin.site.register(AlpinistInGroup)
