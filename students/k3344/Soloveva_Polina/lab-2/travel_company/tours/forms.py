from datetime import date
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Booking, Review, Tour, Tariff, MealOption
from django.contrib.auth.forms import AuthenticationForm
from .models import Tour
from django.forms.models import inlineformset_factory
from django import forms


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = [
            'hotel',
            'stars',
            'agency',
            'country',
            'city',
            'description',
            'start_date',
            'end_date',
            'payment_conditions',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),  # Календарь для start_date
            'end_date': forms.DateInput(attrs={'type': 'date'}),    # Календарь для end_date
        }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        today = date.today()
        if start_date < today:
            raise forms.ValidationError("Start date must be today or later.")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date < self.cleaned_data.get('start_date'):
            raise forms.ValidationError("End date cannot be before start date.")
        return end_date


class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['name', 'price']


class MealOptionForm(forms.ModelForm):
    class Meta:
        model = MealOption
        fields = ['name', 'price']


# Inline formsets для Tariff и MealOption
TariffFormSet = inlineformset_factory(
    Tour, Tariff, form=TariffForm, extra=1, can_delete=True
)
MealOptionFormSet = inlineformset_factory(
    Tour, MealOption, form=MealOptionForm, extra=1, can_delete=True
)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['num_people', 'tariff', 'meal_option']

    def __init__(self, *args, **kwargs):
        tour = kwargs.pop('tour', None)
        super().__init__(*args, **kwargs)

        if tour:
            # Ограничиваем выбор тарифов и вариантов питания
            self.fields['tariff'].queryset = tour.tariffs.all()
            self.fields['meal_option'].queryset = tour.meal_options.all()

            self.fields['tariff'].widget = forms.Select(
                attrs={
                    'class': 'tariff-select',
                },
                choices=[(tariff.id, f'{tariff.name} - {tariff.price} RUB') for tariff in tour.tariffs.all()]
            )
            self.fields['meal_option'].widget = forms.Select(
                attrs={
                    'class': 'meal-select',
                },
                choices=[(meal.id, f'{meal.name} - {meal.price} RUB') for meal in tour.meal_options.all()]
            )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']


class TourSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)

