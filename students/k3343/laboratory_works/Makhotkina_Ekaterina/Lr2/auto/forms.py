from django import forms
from .models import RaceParticipant, Comment, Racer, Team, Car, Fan
from django.contrib.auth.models import User



class UserRoleRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('racer', 'Гонщик'),
        ('fan', 'Болельщик'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Выберите роль', required=True)

    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class RacerRegistrationForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False, label="Команда")
    car = forms.ModelChoiceField(queryset=Car.objects.all(), required=False, label="Автомобиль")
    years_of_experience = forms.IntegerField(label="Опыт (лет)")
    participant_class = forms.ChoiceField(
        choices=[('platinum', 'Платиновый'), ('gold', 'Золотой'), ('silver', 'Серебряный'), ('bronze', 'Бронзовый')],
        label="Статус")
    bio = forms.CharField(widget=forms.Textarea, label="Биография", required=False)

    class Meta:
        model = Racer
        fields = ['team', 'car', 'years_of_experience', 'participant_class', 'bio']

class FanRegistrationForm(forms.ModelForm):
    class Meta:
        model = Fan
        fields = []

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Fan.objects.create(user=user)
        return user


class RaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = RaceParticipant
        fields = ['race', 'racer']


class RaceParticipantForm(forms.ModelForm):
    class Meta:
        model = RaceParticipant
        fields = ['race', 'racer']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class RacerProfileForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['team', 'car', 'bio', 'years_of_experience', 'participant_class', 'status']


class RacerForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['team', 'car', 'bio', 'years_of_experience', 'participant_class', 'status']
