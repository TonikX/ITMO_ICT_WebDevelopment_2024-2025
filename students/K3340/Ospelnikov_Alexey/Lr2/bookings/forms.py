from django import forms
from .models import Booking
from django.forms import DateInput

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date']
        widgets = {
          'check_in_date': DateInput(attrs={'type':'date'}),
          'check_out_date': DateInput(attrs={'type':'date'}),
        }