from django import forms

from hotel_app import models


class CreateReservationForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = ["start_date", "end_date"]

    start_date = forms.DateField(
        label="Дата начала",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    end_date = forms.DateField(
        label="Дата окончания",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )


class UpdateReservationForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = ["start_date", "end_date"]

    start_date = forms.DateField(
        label="Дата начала",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    end_date = forms.DateField(
        label="Дата окончания",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["rating", "comment"]

    comment = forms.CharField(
        label="Напишите ваш отзыв",
        required=True,
        widget=forms.Textarea(attrs={"cols": 100, "rows": 5})
    )
    rating = forms.ChoiceField(
        label="Оцените номер",
        required=True,
        choices=[(i, i) for i in range(10, 0, -1)],
    )
