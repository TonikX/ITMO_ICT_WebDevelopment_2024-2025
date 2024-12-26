from django import forms
from tour.models import Tour, Review

class TourForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите название тура'
    }))
    agency = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите название вашего агенства'
    }))
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите описание вашего тура'
    }))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    payment_terms = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите условия оплаты'
    }))
    price = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0, widget=forms.NumberInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите цену'
    }))

    class Meta:
        model = Tour
        fields = ('name', 'agency', 'description', 'start_date', 'end_date', 'payment_terms', 'price')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'placeholder': 'Оценка от 1 до 5'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Напишите ваш отзыв'}),
        }