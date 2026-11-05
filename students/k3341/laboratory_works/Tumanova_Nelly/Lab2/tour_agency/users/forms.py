from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from .models import User

class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'


class UserLoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Логин"
        self.fields['password'].label = "Пароль"


class UserRegisterForm(StyledFormMixin, UserCreationForm):
    first_name = forms.CharField(label="Ваше имя", required=True)
    last_name = forms.CharField(label="Ваша фамилия", required=True)
    email = forms.EmailField(label="Электронная почта", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Логин для входа',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Придумайте пароль"
        self.fields['password2'].label = "Повторите пароль"


class ProfileEditForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
        }


class UserPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Старый пароль"
        self.fields['new_password1'].label = "Новый пароль"
        self.fields['new_password2'].label = "Подтвердите новый пароль"
