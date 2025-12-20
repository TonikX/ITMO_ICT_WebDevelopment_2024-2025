from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review, Tour

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating', 'tour_start_date', 'tour_end_date']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'tour_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tour_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию, описанию или стране...'
        }),
        label=''
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамически получаем список стран из базы данных
        countries = Tour.objects.values_list('country', flat=True).distinct().order_by('country')
        country_choices = [('', 'Все страны')] + [(country, country) for country in countries]
        self.fields['country'] = forms.ChoiceField(
            required=False,
            choices=country_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Страна'
        )