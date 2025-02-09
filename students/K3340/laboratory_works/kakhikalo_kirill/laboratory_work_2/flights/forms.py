from django import forms
from .models import Reservation, Comment


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['seat', 'service_class', 'name', 'surname']
        widgets = {
            'seat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер места'}),
            'service_class': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('economy', 'Эконом'),
                ('business', 'Бизнес'),
                ('first', 'Первый'),
            )),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
        }


class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Рейтинг от 1 до 10'})
    )

    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш отзыв'}),
        }
