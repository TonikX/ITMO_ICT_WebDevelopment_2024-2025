from django import forms


class SignInForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")

    password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput,
        label="Пароль",
    )

    def clean_email(self):
        email: str = self.cleaned_data["email"]
        return email.strip()


class SignUpForm(SignInForm):
    first_name = forms.CharField(required=True, label="Имя")

    last_name = forms.CharField(required=True, label="Фамилия")

    confirm_password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput,
        label="Повторите пароль",
    )

    field_order = (
        "first_name",
        "last_name",
        "email",
        "password",
        "confirm_password",
    )

    def clean_first_name(self):
        first_name: str = self.cleaned_data["first_name"]
        if not first_name:
            raise forms.ValidationError("Фамилия не должна быть пустой строкой")

        return first_name.strip()

    def clean_last_name(self):
        last_name: str = self.cleaned_data["last_name"]
        if not last_name:
            raise forms.ValidationError("Имя не должно быть пустым значением")

        return last_name.strip()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
