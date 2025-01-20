from django import forms

from .models import Student, Assignment


class SignUpStudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = [
            'name',
            'username',
            'password',
        ]

    def clean(self):
        cleaned = super().clean()
        original_password = cleaned.get("password")
        confirm_password = cleaned.get("confirm_password")

        if original_password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return cleaned


class SignInStudentForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = [
            'username',
            'password',
        ]


class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['text']
