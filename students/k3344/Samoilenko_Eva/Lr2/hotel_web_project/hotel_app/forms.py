from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Review
from django.contrib.auth.models import User
from django import forms


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = {
            "start_date",
            "end_date"
        }


class ReviewWriteForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = {
            "rate",
            "review"
        }
        widgets = {
            'rate': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.username =
        if commit:
            user.save()
        return user
