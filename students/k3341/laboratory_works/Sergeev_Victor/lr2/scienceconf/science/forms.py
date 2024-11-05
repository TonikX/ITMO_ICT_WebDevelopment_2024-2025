from django import forms

class LoginUserForm(forms.Form):
    username = forms.CharField(required=True, label='Username')
    password = forms.CharField(required=True, min_length=8, label="Password")

class RegistrationForm(LoginUserForm):
    first_name = forms.CharField(required=True, label="First name")
    last_name = forms.CharField(required=True, label="Last name")
    email = forms.EmailField(required=True, label="Email")
    confirm_password = forms.CharField(required=True, min_length=8, label="Confirm password")

    field_order = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def clean_first_name(self):
        first_name: str = self.cleaned_data["first_name"]
        if not first_name:
            raise forms.ValidationError("First name must not be an empty string")

        return first_name.strip()

    def clean_last_name(self):
        last_name: str = self.cleaned_data["last_name"]
        if not last_name:
            raise forms.ValidationError("Last name must not be an empty string")

        return last_name.strip()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password must be equal")

