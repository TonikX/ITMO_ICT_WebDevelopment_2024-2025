from django import forms
from .models import *

class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format="%d/%m/%Y", attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(format="%d/%m/%Y", attrs={'type': 'date'}), required=False)
    add_info = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Booking
        fields = ["start_date", "end_date", "person_count", "add_info"]
        widgets = {"client": forms.HiddenInput(), "room": forms.HiddenInput()}

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("Start date must be before end date")


class ReviewForm(forms.ModelForm):
    rate = forms.IntegerField(label="Your Rate", widget=forms.NumberInput(attrs={'type': 'number'}))
    description = forms.CharField(label="Description", widget=forms.Textarea, required=False)
    class Meta:
        model = Review
        fields = ["rate", "description"]
        widgets = {"client": forms.HiddenInput(), "hotel": forms.HiddenInput()}

    def clean(self):
        rate = self.cleaned_data.get('rate')
        if rate < 1 or rate > 10:
            raise forms.ValidationError("Rate must be between 1 and 10")
