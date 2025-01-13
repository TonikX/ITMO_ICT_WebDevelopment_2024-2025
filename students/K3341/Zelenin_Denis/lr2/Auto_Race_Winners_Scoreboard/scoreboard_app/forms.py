from django.contrib.auth.forms import UserCreationForm
from .models import User, Comments, Race
from .models import Driver
from .models import Car
from .models import Truck
from django import forms



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',  'password1', 'password2')


class AddCommentForm(forms.ModelForm):
    OPTIONS = [
        ('cooperation', 'Cooperation'),
        ('race', 'Race'),
        ('other', 'Other'),
    ]

    com_type = forms.ChoiceField(
        choices=OPTIONS,
        label="Choose option",
        widget=forms.Select,
    )

    class Meta:
        model = Comments
        fields = ['com_type', 'comment']


class AddDriver(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['car_id', 'first_name', 'last_name', 'number', 'team', 'experience', 'grade']


class AddCar(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class AddTruck(forms.ModelForm):

    class Meta:
        model = Truck
        fields = '__all__'


class AddRace(forms.ModelForm):

    class Meta:
        model = Race
        fields = '__all__'
