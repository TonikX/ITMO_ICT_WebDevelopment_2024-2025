from django.contrib.admin.helpers import forms
from django.contrib.auth.forms import UserCreationForm

from Conference.models import User, PresentationRegistration, Review


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'education', 'phone_number']

class PresentationRegistrationForm(forms.ModelForm):
    class Meta:
        model = PresentationRegistration
        fields = ['title', 'abstract']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']