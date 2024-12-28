from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Review, Registration


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']  # Updated to match your Review model fields
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 4}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 11)]),  # Use Select for rating choices
        }
        labels = {
            'comment': 'Review Comment',  # Updated label
            'rating': 'Rating',  # Label remains the same
        }
        help_texts = {
            'rating': 'Please select a rating between 1 and 10.',
        }

class RegistrationEditForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['topic']  # Only allow editing the topic field

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['conference', 'topic']  # Include the topic field
        widgets = {
            'conference': forms.HiddenInput()  # Hide the conference selection if it's pre-determined
        }