import logging
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Car, CarOwner

logger = logging.getLogger(__name__)

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['reg_number', 'brand', 'model_name', 'color_desc']  # Updated fields

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False)  # Updated from birth_date

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'email', 'username', 'passport_id', 'address', 'country'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            logger.info(f"User {user.username} created (type: {type(user)})")
            owner = CarOwner(user=user, date_of_birth=self.cleaned_data['date_of_birth'])
            owner.save()
        return user
