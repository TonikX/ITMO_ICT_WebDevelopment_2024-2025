from django import forms
from .models import Review

class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'


class ReviewForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'text')
        labels = {
            'rating': 'Ваша оценка от 0 до 10',
            'text': 'Текст отзыва',
        }