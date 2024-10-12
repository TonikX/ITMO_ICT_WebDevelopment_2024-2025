from django import forms

from .models import Student, Assignment


class RegisterStudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords must match")
        return cleaned_data


class LoginStudentForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Student
        fields = [
            'email',
            'password',
        ]
        
        
class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['text']



class EditAssignmentForm(CreateAssignmentForm):
    class Meta(CreateAssignmentForm):
        model = Assignment
        fields = ['text']
