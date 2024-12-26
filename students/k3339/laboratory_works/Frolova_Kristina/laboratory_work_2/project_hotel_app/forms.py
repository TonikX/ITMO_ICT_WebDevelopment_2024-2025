from django import forms

from project_hotel_app.models import Reservation, Review


class ReservationUpdateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "start_date",
            "end_date",
        ]

class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "start_date",
            "end_date",
        ]

class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "review",
            "rate"
        ]
        widgets = {
            'review': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'rate': forms.Select(choices=[(i, i) for i in range(1, 11)]),
        }