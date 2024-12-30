from django.contrib.auth.models import User
from django import forms

from travelCompany.models import Review, Tour, TravelAgency


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        labels = {
            'comment': 'Ваш отзыв',
            'rating': 'Оценка'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
        }


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['start_date', 'end_date']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 5:
            raise forms.ValidationError("Название тура должно быть длиннее 5 символов.")
        return name


class CreateAgency(forms.ModelForm):
    class Meta:
        model = TravelAgency
        fields = ['name', 'description', 'contact_info','address','number']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 5:
            raise forms.ValidationError("Название тура должно быть длиннее 5 символов.")
        return name


class CreateTour(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'agency', 'description', 'start_date', 'end_date', 'payment_conditions', 'country']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 5:
            raise forms.ValidationError("Название тура должно быть длиннее 5 символов.")
        return name