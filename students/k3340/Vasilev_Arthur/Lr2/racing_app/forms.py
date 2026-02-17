from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Comment, Car, Team

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 
                 'experience', 'driver_class', 'bio']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'type', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите ваш комментарий...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
        labels = {
            'text': 'Текст комментария',
            'type': 'Тип комментария',
            'rating': 'Рейтинг (1-10)',
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'team', 'description', 'year']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'year': forms.NumberInput(attrs={'min': 1900, 'max': 2024}),
        }