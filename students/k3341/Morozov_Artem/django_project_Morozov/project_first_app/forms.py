from django import forms

from project_first_app.models import Owner, ExampleModel


class ExampleForm(forms.ModelForm):
    class Meta:
        # specify model to be used
        model = ExampleModel

        # specify fields to be used
        fields = [
            "title",
            "description",
        ]

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'soname', 'birthday']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }