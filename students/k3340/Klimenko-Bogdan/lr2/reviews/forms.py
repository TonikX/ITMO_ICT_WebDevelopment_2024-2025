from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['stay_start', 'stay_end', 'comment', 'rating']
        widgets = {
            'stay_start': forms.DateInput(attrs={'type': 'date'}),
            'stay_end': forms.DateInput(attrs={'type': 'date'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }