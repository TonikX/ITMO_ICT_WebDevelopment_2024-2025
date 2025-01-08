from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(max_length=255, required=False)


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", "phone_number", "date_of_birth", "address")


class SignInForm(AuthenticationForm):
    pass