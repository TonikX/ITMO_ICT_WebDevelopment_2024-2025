from django import forms
from .models import Tour, Departure


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'


class TourForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('title', 'countries', 'description')
        labels = {
            'title': 'Название тура',
            'countries': 'Страны тура',
            'description': 'Описание тура',
        }

class DepartureForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Departure
        fields = ('start_date', 'end_date')
        labels = {
            'start_date': 'Дата начала поездки',
            'end_date': 'Дата окончания поездки',
        }