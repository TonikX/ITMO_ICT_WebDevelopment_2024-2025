from django import forms
from .models import Review, Reservation, User
from django.contrib.auth.forms import UserCreationForm


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating'] 
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Введите ваш отзыв'}),
            'rating': forms.Select(),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['seat_number', 'ticket_number']  

class UserForm(UserCreationForm):
    passport = forms.CharField(max_length=20, required=False, label='Номер паспорта')
    birth_date = forms.DateField(required=False, label='Дата рождения', widget=forms.SelectDateWidget(years=range(1900, 2025)))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'passport', 'birth_date')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user              