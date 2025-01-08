from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Participant, Race, Team, Comment

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)
    experience = forms.IntegerField(label="Опыт (в годах)", min_value=0, required=True) 

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "role", "experience"] 

class ParticipantProfileForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['full_name', 'team', 'car_description', 'participant_description', 'experience', 'race_class']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.all()

class RaceRegistrationForm(forms.Form):
    race = forms.ModelChoiceField(queryset=Race.objects.all(), label="Выберите гонку")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите ваш комментарий...'}),
            'comment_type': forms.Select(choices=Comment.COMMENT_TYPE_CHOICES),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
        labels = {
            'text': 'Комментарий',
            'comment_type': 'Тип комментария',
            'rating': 'Рейтинг (1-10)',
        }
