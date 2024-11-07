from django import forms
from django.forms.widgets import HiddenInput
from science import models

class LoginUserForm(forms.Form):
    username = forms.CharField(required=True, label='Username')
    password = forms.CharField(required=True, min_length=8, label="Password")

class RegistrationForm(LoginUserForm):
    first_name = forms.CharField(required=True, label="First name")
    last_name = forms.CharField(required=True, label="Last name")
    email = forms.EmailField(required=True, label="Email")
    confirm_password = forms.CharField(required=True, min_length=8, label="Confirm password")

    field_order = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def clean_first_name(self):
        first_name: str = self.cleaned_data["first_name"]
        if not first_name:
            raise forms.ValidationError("First name must not be an empty string")

        return first_name.strip()

    def clean_last_name(self):
        last_name: str = self.cleaned_data["last_name"]
        if not last_name:
            raise forms.ValidationError("Last name must not be an empty string")

        return last_name.strip()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password must be equal")

class ConferenceRegisterForm(forms.Form):
    name = forms.CharField(max_length=150, required=True, label='Name')
    description = forms.CharField(max_length=500, label='Description')
    participate_conditionals = forms.CharField(max_length=500, label='Speaker requirements')
    location = forms.CharField(max_length=150, required=True)
    date_of_start = forms.DateTimeField(required=True, label="Date of start")
    date_of_finish = forms.DateTimeField(required=True, label="Date of finish")
    field_order = ['name',
                   'description',
                   'participate_conditionals',
                   'location',
                   'date_of_start',
                   'date_of_finish']
    
    def clean_name(self):
        name: str = self.cleaned_data["name"]
        if not name:
            raise forms.ValidationError("Name must not be an empty string")

        return name.strip()

    def clean_location(self):
        location: str = self.cleaned_data["location"]
        if not location:
            raise forms.ValidationError("Location must not be an empty string")

        return location.strip()

class SpeakerRegisterForm(forms.Form):
    topic = forms.CharField(required=True, label="Speaking topic")
    recommended = forms.BooleanField(required=False, widget=HiddenInput)

class ReviewForm(forms.Form):
    grade = forms.IntegerField(min_value=1, max_value=10, label='Grade')
    description = forms.CharField(max_length=1000, label="Feedback")

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Commentary
        fields = ('description',)
