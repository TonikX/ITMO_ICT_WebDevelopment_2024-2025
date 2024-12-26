from django.contrib import admin

from Hospital.models import Patient, Doctor, Appointment, Cabinet, Service, Payment, MedicalCard, DoctorSchedule

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Cabinet)
admin.site.register(Service)
admin.site.register(Payment)
admin.site.register(MedicalCard)
admin.site.register(DoctorSchedule)