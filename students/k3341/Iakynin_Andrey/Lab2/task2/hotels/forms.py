from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from hotels.models import Profile, Hotel, Booking, Review, Room


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    is_owner = forms.BooleanField(label='Are you a hotel owner?', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'is_owner')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, is_owner=self.cleaned_data['is_owner'])
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class FavoriteForm(forms.ModelForm):
    hotel_id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Hotel
        fields = []


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        if check_in and check_out and check_in >= check_out:
            raise ValidationError("Дата заезда должна быть раньше даты выезда.")

        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text","rating"]


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["name", "address",]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['type', 'price']



