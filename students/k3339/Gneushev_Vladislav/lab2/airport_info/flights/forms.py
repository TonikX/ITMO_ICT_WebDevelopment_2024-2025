from django import forms

from .models import Ticket, FlightReview, TicketReservation


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_number']


class TicketReservationForm(forms.ModelForm):
    class Meta:
        model = TicketReservation
        fields = []

    def __init__(self, *args, **kwargs):
        self.flight = kwargs.pop('flight', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        passenger = self.instance.passenger
        if TicketReservation.objects.filter(flight=self.flight, passenger=passenger).exists():
            raise forms.ValidationError("You have already reserved a ticket for this flight.")
        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = FlightReview
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
        labels = {
            'text': 'Review',
            'rating': 'Rating (1 to 10)',
        }
