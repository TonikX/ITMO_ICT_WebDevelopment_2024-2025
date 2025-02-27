from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Review, Registration


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['topic']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['user'] = forms.ModelChoiceField(
                queryset=user,
                initial=user,
                widget=forms.HiddenInput()
            )