from django import forms
from .models import UserProfile, Submission

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, label="Роль")

    class Meta:
        model = UserProfile
        fields = ['username', 'role', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_text']