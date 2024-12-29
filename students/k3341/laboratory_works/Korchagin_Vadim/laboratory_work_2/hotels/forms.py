from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Review

# Форма регистрации нового пользователя
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # Поля, которые будут отображаться в форме регистрации
        fields = ('username', 'email', 'password1', 'password2')

    # Переопределение метода save для сохранения email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Форма для создания нового бронирования
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        # Устанавливаем виджеты для отображения календаря в полях выбора даты
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    # Переопределение конструктора для дополнительного параметра room
    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)

    # Проверка даты начала и окончания бронирования
    def clean(self):
        cleaned_data = super().clean()  # Получаем "очищенные" данные из формы, которые уже прошли базовую проверку Django.
        start_date = cleaned_data.get('start_date')  # Извлекаем поле start_date из очищенных данных.
        end_date = cleaned_data.get('end_date')  # Извлекаем поле end_date из очищенных данных.

        # Проверка на существующие бронирования для данной комнаты
        if start_date and end_date and self.room:
            # Проверяем, существуют ли пересекающиеся бронирования для выбранной комнаты
            existing_bookings = Booking.objects.filter(
                room=self.room,
                start_date__lte=end_date,
                end_date__gte=start_date
            ).exclude(pk=self.instance.pk if self.instance.pk else None)

            if existing_bookings.exists():
                raise forms.ValidationError('Комната уже забронирована на выбранные даты')

        return cleaned_data

# Форма для добавления отзыва на бронирование
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']