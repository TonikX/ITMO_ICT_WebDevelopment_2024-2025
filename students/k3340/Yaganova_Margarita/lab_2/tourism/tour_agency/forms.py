from django import forms
from .models import TourBooking, Tourist, Review, Country, Tour
from django.contrib.auth.forms import UserCreationForm


class TouristRegistrationForm(UserCreationForm):
    class Meta:
        model = Tourist
        fields = ('email', 'username', 'password1', 'password2')


class BookingForm(forms.ModelForm):
    tour_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        tour_id = kwargs.pop('tour_id', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        if tour_id:
            tour = Tour.objects.get(pk=tour_id)
            available_dates = [(date, date) for date in tour.available_dates]
            hotel_categories = [(category, category) for category in
                                tour.hotel_category]
            self.fields['selected_date'] = forms.ChoiceField(
                label='Выберите дату',
                choices=available_dates,
                widget=forms.Select(
                    attrs={'class': 'form-control'}))
            self.fields['selected_category'] = forms.ChoiceField(
                label='Категория отеля',
                choices=hotel_categories,
                widget=forms.Select(
                    attrs={'class': 'form-control'}))

    persons_number = forms.IntegerField(label='Количество взрослых',
                                        widget=forms.NumberInput(
                                            attrs={'class': 'form-control'}))

    children_number = forms.IntegerField(label='Количество детей',
                                         widget=forms.NumberInput(
                                             attrs={'class': 'form-control'}))
    rooms_number = forms.IntegerField(label='Количество номеров',
                                      widget=forms.NumberInput(
                                          attrs={'class': 'form-control'}))

    class Meta:
        model = TourBooking
        exclude = ('status', 'tourist', 'tour')


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('rating','text')


class CountrySelectionForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(),
                                     label='Выберите страну')
