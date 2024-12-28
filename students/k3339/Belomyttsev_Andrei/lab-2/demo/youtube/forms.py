from django import forms
from .models import Channel, Review

class AddChannelForm(forms.ModelForm):
  class Meta:
    model = Channel
    fields = ['url', 'lang', 'category', 'theme']

class AddReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    fields = ['rating', 'text']