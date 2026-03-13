from django.contrib import admin
from .models import (
    FeedingRationType, FeedingRation, Habitat, Zoo, WinteringPlace,
    Department, Building, Enclosure, Staff, Animal, FeedingHistory,
    CaretakerAssignment, VeterinarianAssignment, TransferHistory
)

admin.site.register(FeedingRationType)
admin.site.register(FeedingRation)
admin.site.register(Habitat)
admin.site.register(Zoo)
admin.site.register(WinteringPlace)
admin.site.register(Department)
admin.site.register(Building)
admin.site.register(Enclosure)
admin.site.register(Staff)
admin.site.register(Animal)
admin.site.register(FeedingHistory)
admin.site.register(CaretakerAssignment)
admin.site.register(VeterinarianAssignment)
admin.site.register(TransferHistory)