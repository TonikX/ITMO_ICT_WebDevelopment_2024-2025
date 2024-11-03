from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Registration, Review, Presentation


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super(BootstrapFormMixin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(max_length=255, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PresentationForm(BootstrapFormMixin, forms.ModelForm):
    name = forms.CharField(required=False, label="Название презентации")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Описание презентации")
    duration = forms.IntegerField(required=False, label="Длительность (в минутах)")

    class Meta:
        model = Presentation
        fields = ['name', 'description', 'duration']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RegistrationUpdateForm(forms.ModelForm):
    is_author = forms.BooleanField(required=False, label="Является автором")

    name = forms.CharField(required=False, label="Название презентации")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Описание презентации")
    duration = forms.IntegerField(required=False, label="Длительность (в минутах)")

    class Meta:
        model = Registration
        fields = ['is_author']

    def __init__(self, *args, **kwargs):
        registration = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if registration and registration.is_author and registration.presentation:
            self.fields['name'].initial = registration.presentation.name
            self.fields['description'].initial = registration.presentation.description
            self.fields['duration'].initial = registration.presentation.duration

    def clean(self):
        cleaned_data = super().clean()
        is_author = cleaned_data.get("is_author")

        if is_author:
            if not cleaned_data.get("name") or not cleaned_data.get("description") or not cleaned_data.get("duration"):
                raise forms.ValidationError("Пожалуйста, заполните все поля для редактирования презентации.")

        return cleaned_data

    def save(self, commit=True):
        registration = super().save(commit=False)
        is_author = self.cleaned_data.get("is_author")

        if is_author:
            if not registration.presentation:
                presentation = Presentation.objects.create(
                    name=self.cleaned_data.get("name"),
                    description=self.cleaned_data.get("description"),
                    duration=self.cleaned_data.get("duration"),
                    conference=registration.conference,
                    author=registration.user
                )
                registration.presentation = presentation
            else:
                registration.presentation.name = self.cleaned_data.get("name")
                registration.presentation.description = self.cleaned_data.get("description")
                registration.presentation.duration = self.cleaned_data.get("duration")
                registration.presentation.save()

        if commit:
            registration.save()

        return registration


class ReviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
