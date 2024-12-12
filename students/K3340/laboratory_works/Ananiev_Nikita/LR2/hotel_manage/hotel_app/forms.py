from django import forms
from .models import HotelPicture, RoomPicture

class HotelPictureForm(forms.ModelForm):
    class Meta:
        model = HotelPicture
        fields = ['image']
        widgets = {"hotel": forms.HiddenInput()}

class RoomPictureForm(forms.ModelForm):
    class Meta:
        model = RoomPicture
        fields = ['image']
        widgets = {"room": forms.HiddenInput()}
