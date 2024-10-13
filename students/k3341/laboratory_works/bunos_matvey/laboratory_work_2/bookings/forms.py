from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super(BootstrapFormMixin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ReservationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'check_out': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['check_in'].input_formats = ['%Y-%m-%d']
        self.fields['check_out'].input_formats = ['%Y-%m-%d']

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out and check_in >= check_out:
            raise forms.ValidationError('Дата выезда должна быть позже даты заезда.')

        conflicts = Reservation.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()
        if conflicts:
            raise forms.ValidationError('Номер недоступен на выбранные даты.')


class ReviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
