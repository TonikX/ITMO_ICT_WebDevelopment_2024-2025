from django import forms
from flights.models import PassengerRegistration, Feedback


class ReserveSeatForm(forms.ModelForm):
    seat = forms.CharField(max_length=3)

    class Meta:
        model = PassengerRegistration
        fields = ("seat",)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("text", "rating")
