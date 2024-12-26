from django import forms
from django.contrib.auth.models import User
from .models import Comment

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don’t match.')
        return cd['password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']  # Поля, которые пользователь будет заполнять
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите ваш комментарий...'}),
            'comment_type': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
        }
        labels = {
            'text': 'Комментарий',
            'comment_type': 'Тип комментария',
            'rating': 'Рейтинг',
        }
