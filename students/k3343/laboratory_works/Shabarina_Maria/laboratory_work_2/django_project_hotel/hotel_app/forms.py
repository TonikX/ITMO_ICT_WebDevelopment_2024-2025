from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Hotel
from .models import Review


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=[('user', 'Regular User'), ('admin', 'Hotel Admin')],
        required=True
    )
    managed_hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), required=False)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'managed_hotel')
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'user_type': forms.Select(),
            'managed_hotel': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'email', 'password1', 'password2']:
            self.fields[field].help_text = None

        if self.instance and self.instance.user_type == 'admin':
            self.fields['managed_hotel'].required = True


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
