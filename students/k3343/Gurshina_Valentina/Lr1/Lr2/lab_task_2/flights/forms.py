# Форма авторизации на основе встроенной в Django

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("last_name", "first_name", "username", "email", "password1", "password2")

    last_name = forms.CharField(label="Фамилия", required=True)
    first_name = forms.CharField(label="Имя", required=True) #отметка обязательности
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False) #чтобы не отправлялся запрос в БД
        user.last_name = self.cleaned_data["last_name"]
        user.first_name = self.cleaned_data["first_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# ОТЗЫВ И ОБРАТНАЯ СВЯЗЬ 

from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text', 'rating'] #от 0 до 5. Форма, основанная на модели 
