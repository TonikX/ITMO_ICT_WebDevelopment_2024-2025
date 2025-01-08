from django import forms
from .models import Review
from django.forms import DateInput

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['room', 'comment', 'rating', 'stay_start', 'stay_end']
        widgets = {
            'stay_start': DateInput(attrs={'type':'date'}),
            'stay_end': DateInput(attrs={'type':'date'}),
        }