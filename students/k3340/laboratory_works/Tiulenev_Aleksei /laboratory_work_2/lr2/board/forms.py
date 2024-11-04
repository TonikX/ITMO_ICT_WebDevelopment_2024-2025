from django import forms
from .models import Student, Assignment

class SignUpStudentForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите пароль'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Подтвердите пароль'
        })
    )

    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите ваше имя'
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите имя пользователя'
        })
    )

    class Meta:
        model = Student
        fields = [
            'name',
            'username',
            'password',
        ]

    def clean(self):
        cleaned = super().clean()
        original_password = cleaned.get("password")
        confirm_password = cleaned.get("confirm_password")

        if original_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned


class SignInStudentForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите пароль'
        })
    )

    # Удалён Meta класс, так как forms.Form не требует его


class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['text']
        
