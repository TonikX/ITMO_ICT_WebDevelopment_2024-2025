from datetime import date, timedelta

from django import forms

from conferences.models import Booking, Conference, Feedback


class ConferenceRegistrationForm(forms.ModelForm):
    topics = forms.MultipleChoiceField(
        choices=[(topic.name, topic.value) for topic in Conference.Topic],
        widget=forms.CheckboxSelectMultiple,
        label="Тематики",
    )

    booking = forms.ModelChoiceField(
        queryset=Booking.objects.none(),
        widget=forms.Select,
        label="Бронь на ближайшее время",
        required=True,
    )

    class Meta:
        model = Conference
        fields = (
            "name",
            "description",
            "participation_conditions",
            "topics",
            "booking",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["booking"].queryset = (
            Booking.objects.select_related("room")
            .filter(
                conference__isnull=True,
                start_date__date__range=(
                    date.today(),
                    date.today() + timedelta(days=10),
                ),
            )
            .only("id", "start_date", "end_date", "room__name")
            .order_by("start_date")
        )


class ConferenceUpdatingForm(forms.ModelForm):
    topics = forms.MultipleChoiceField(
        choices=[(topic.name, topic.value) for topic in Conference.Topic],
        widget=forms.CheckboxSelectMultiple,
        label="Тематики",
    )

    class Meta:
        model = Conference
        fields = (
            "name",
            "description",
            "participation_conditions",
            "topics",
        )


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("text", "rating")
        widgets = {
            "text": forms.Textarea(attrs={"maxlength": 250, "required": True}),
            "rating": forms.TextInput(
                attrs={
                    "min": 1,
                    "max": 10,
                    "required": True,
                    "type": "number",
                }
            ),
        }
