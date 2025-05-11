from django import forms

from .models import Conference, ConferenceRating


class ConferenceForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Conference
        fields = ['title', 'topics', 'location', 'start_date', 'end_date', 'description', 'participation_conditions']


class ConferenceRatingForm(forms.ModelForm):
    class Meta:
        model = ConferenceRating
        fields = ['review', 'rating']
